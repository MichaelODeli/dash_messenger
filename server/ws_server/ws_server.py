from quart import websocket, Quart, abort
import ast
import datetime
import psycopg2
import uuid
import traceback

"""
Используемые функции
"""
def db_connector(
    dbname="messenger",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432",
):
    return psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

def get_current_date_str(plus5days=False):
    "Получить текущую дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_plus5days = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    return now_plus5days if plus5days else now

def cred_checker_with_token_generator(conn, username, password):
    "Проверка учетных данных пользователя и выдача токена"
    with conn.cursor() as cursor:
        # проверка существования пользователя в базе
        cursor.execute(
            "SELECT id FROM users WHERE username=%(username)s and password=%(password)s;",
            {"username": username, "password": password},
        )
        result = cursor.fetchone()
        if result != None:
            user_exist = True
            user_id = result[0]
            token = str(uuid.uuid4())
            cursor.execute(
                'INSERT INTO "tokens" ("token", "user_id", "status", "valid_until") values (%(token)s, %(user_id)s, %(status)s, %(valid_until)s)',
                {
                    "token": token,
                    "user_id": user_id,
                    "status": "given",
                    "valid_until": get_current_date_str(plus5days=True),
                },
            )
            conn.commit()
        else:
            user_exist = False
            token = None
    return user_exist, token

def token_validation(conn, token, logout=False):
    """Проверка валидности токена. Валидный - срок действия продлевается.\n
    Также тут будут удаляться старые (недействующие) токены других юзеров."""
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT token FROM tokens WHERE token=%(token)s and valid_until >= %(now)s;",
            {"token": token, 'now': get_current_date_str()},
        )
        result = cursor.fetchone()
        if type(result) != type(None) and token in result:
            if logout==False:
                cursor.execute(
                    "UPDATE tokens SET valid_until = %(valid_time)s WHERE token = %(token)s",
                    {"valid_time": get_current_date_str(plus5days=True), "token": token},
                )
                conn.commit()
                return_res = True
            else:
                cursor.execute("DELETE FROM tokens WHERE token = %(token)s", {"token": token})
                conn.commit()
                return_res = True
        else:
            return_res = False
        
        cursor.execute("DELETE FROM tokens WHERE valid_until <= %(now)s", {"now": get_current_date_str()})
        conn.commit()
    
    return return_res

def get_userid_by_token(conn, token):
    "Получение id пользователя по его токену"
    # if token_validation(conn, token):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT user_id FROM tokens WHERE token=%(token)s and valid_until >= %(now)s;",
            {"token": token, 'now': get_current_date_str()},
        )
        result = cursor.fetchone()
        return result[0] if result != None else None
    # else:
    #     return None


def get_username_by_userid(conn, user_id):
    "Получение имени пользователя по его id"
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT username FROM users WHERE id=%(user_id)s;",
            {"user_id": user_id},
        )
        result = cursor.fetchone()
        return result[0] if result != None else None


def getchats(conn, token):
    "Получение перечня чатов пользователя"
    chats = []
    with conn.cursor() as cursor:
        user_id = get_userid_by_token(conn, token)
        cursor.execute(
            "select chat_id from chat_members cm where user_id = %(user_id)s;",
            {"user_id": user_id},
        )
        chats_ids = cursor.fetchall()
        if chats_ids != None:
            for chat_id in chats_ids:
                chat_id = chat_id[0]
                # основные свойства чата
                cursor.execute(
                    "select * from chats cm where id = %(chat_id)s limit 1;",
                    {"chat_id": chat_id},
                )
                chat_properties = cursor.fetchone()

                # тип чата
                chat_type = 'personal' if chat_properties[2] else 'group'

                # участник(и) чата
                cursor.execute(
                    "select user_id from chat_members cm where chat_id = %(chat_id)s;",
                    {"chat_id": chat_id},
                )
                chat_members = [i[0] for i in cursor.fetchall()]
                chat_members.remove(user_id)

                # название чата
                if chat_type == 'personal':
                    chat_name = get_username_by_userid(conn, chat_members[0])
                else:
                    chat_name = chat_properties[1]

                chats.append(
                    {
                        "chat_id": chat_id,
                        "chat_members": chat_members[0] if chat_type == 'personal' else ','.join(chat_members),
                        "chat_name": chat_name,
                        "chat_type": chat_type,
                        "last_message_time": chat_properties[4].strftime("%Y-%m-%d %H:%M:%S"),
                        "last_message_text": 'not implemented',
                        "last_message_sender": 'not implemented',
                    }
                )
            return chats
        else:
            return None

def getmessages(conn, token, chat_id):
    "Получение перечня чатов пользователя"
    with conn.cursor() as cursor:
        messages = []
        user_id = get_userid_by_token(conn, token)
        cursor.execute(
            "SELECT * FROM messages WHERE chat_id=%(chat_id)s;",
            {"chat_id": chat_id}
        )
        for message_row in cursor.fetchall():
            messages.append(
                {
                    'from_id': message_row[1], 
                    'from_name': get_username_by_userid(conn, message_row[1]), 
                    'content': message_row[3], 
                    'content_type': message_row[4],
                    'content_time': message_row[5].strftime("%Y-%m-%d %H:%M:%S")
                }
            )
        return messages


"""
Основная логика работы сервера

"""

app = Quart(__name__)
@app.websocket("/ws")
async def ws():
    await websocket.accept()
    while True:
        msg = await websocket.receive()
        try:
            conn = db_connector() # подключаемся к БД
            msg_body = ast.literal_eval(msg)
            mode = msg_body["mode"]
            if mode == "auth":
                # авторизация пользователя. успех - токен и 200, провал - None и 401
                cred_checker_result = cred_checker_with_token_generator(
                    conn, msg_body["username"], msg_body["password"]
                ) # проверяем авторизационные данные
                correct_cred = cred_checker_result[0]
                token = cred_checker_result[1]

                # формируем тело сообщения и отправляем тому, кто запросил
                new_msg_body = {
                    "mode": "auth",
                    "timestamp": get_current_date_str(),
                    "status": "200" if correct_cred else "401",
                    "token": (token if correct_cred else None),
                }
                await websocket.send(str(new_msg_body))
            elif mode == 'logout':
                if token_validation(conn, msg_body["token"], logout=True):
                    success = True
                else:
                    success = False
                new_msg_body = {
                    "mode": "logout",
                    "timestamp": get_current_date_str(),
                    "status": "200" if success else "401",
                }
                await websocket.send(str(new_msg_body))
            elif mode == 'getChats':
                if token_validation(conn, msg_body["token"]):
                    success = True
                    chats = getchats(conn, msg_body["token"])
                else:
                    success = False
                    chats = ''
                new_msg_body = {
                    "mode": "getChats",
                    "timestamp": get_current_date_str(),
                    "status": "200" if success else "401",
                    'chats': chats if success else None
                }
                await websocket.send(str(new_msg_body))
            elif mode == 'getMessages':
                if token_validation(conn, msg_body["token"]):
                    success = True
                    messages = getmessages(conn, msg_body["token"], msg_body["chat_id"])
                else:
                    success = False
                    messages = ''
                new_msg_body = {
                    "mode": "getMessages",
                    "timestamp": get_current_date_str(),
                    "status": "200" if success else "401",
                    'chats': messages if success else None
                }
                await websocket.send(str(new_msg_body))
            else:
                await websocket.send(
                    str(
                        {"mode": mode, "timestamp": None, "status": "501"}
                    )  # not implemented
                )
        except Exception as e:
            print(traceback.format_exc())
            return abort(500)


if __name__ == "__main__":
    app.run(port=5000)
