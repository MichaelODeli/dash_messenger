from quart import websocket, Quart, abort
import ast
import datetime
import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION, FOREIGN_KEY_VIOLATION
import uuid
import traceback
import os

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
    SECRET_KEY = os.environ.get("AM_I_IN_A_DOCKER_CONTAINER", False)
    if SECRET_KEY:
        host = "db"

    return psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )


def get_current_date_str(plus5days=False):
    "Получить текущую дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_plus5days = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
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
        # # check token counts
        # if token_count == 5:
        #     raise AssertionError
        cursor.execute(
            "SELECT token FROM tokens WHERE token=%(token)s and valid_until >= %(now)s;",
            {"token": token, "now": get_current_date_str()},
        )
        result = cursor.fetchone()
        if type(result) != type(None) and token in result:
            if logout == False:
                cursor.execute(
                    "UPDATE tokens SET valid_until = %(valid_time)s WHERE token = %(token)s",
                    {
                        "valid_time": get_current_date_str(plus5days=True),
                        "token": token,
                    },
                )
                conn.commit()
                return_res = True
            else:
                cursor.execute(
                    "DELETE FROM tokens WHERE token = %(token)s", {"token": token}
                )
                conn.commit()
                return_res = True
        else:
            return_res = False

        cursor.execute(
            "DELETE FROM tokens WHERE valid_until <= %(now)s",
            {"now": get_current_date_str()},
        )
        conn.commit()

    return return_res


def get_userid_by_token(conn, token):
    "Получение id пользователя по его токену"
    # if token_validation(conn, token):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT user_id FROM tokens WHERE token=%(token)s and valid_until >= %(now)s;",
            {"token": token, "now": get_current_date_str()},
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


def get_userid_by_username(conn, user_name):
    "Получение id пользователя по его нику"
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM users WHERE username=%(user_name)s;",
            {"user_name": user_name},
        )
        result = cursor.fetchone()
        return result[0] if result != None else None


def check_user_membership(conn, user_id, chat_id):
    "Проверка наличия юзера в чате"
    with conn.cursor() as cursor:
        cursor.execute(
            "select EXISTS(SELECT 1 FROM chat_members where chat_id = %(chat_id)s and user_id = %(user_id)s);",
            {"chat_id": chat_id, "user_id": user_id},
        )
        return cursor.fetchone()[0]


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
                chat_type = "personal" if chat_properties[2] else "group"

                # участник(и) чата
                cursor.execute(
                    "select user_id from chat_members cm where chat_id = %(chat_id)s;",
                    {"chat_id": chat_id},
                )
                chat_members = [i[0] for i in cursor.fetchall()]
                chat_members.remove(user_id)

                # название чата
                if chat_type == "personal":
                    chat_name = get_username_by_userid(conn, chat_members[0])
                else:
                    chat_name = chat_properties[1]

                chats.append(
                    {
                        "chat_id": chat_id,
                        "chat_members": (
                            chat_members[0]
                            if chat_type == "personal"
                            else ",".join(chat_members)
                        ),
                        "chat_name": chat_name,
                        "chat_type": chat_type,
                        "last_message_time": chat_properties[4].strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "last_message_text": "not implemented",
                        "last_message_sender": "not implemented",
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
        if not check_user_membership(conn, user_id, chat_id):
            return "423"
        else:
            cursor.execute(
                "SELECT * FROM messages WHERE chat_id=%(chat_id)s;",
                {"chat_id": chat_id},
            )
            for message_row in cursor.fetchall():
                messages.append(
                    {
                        "from_id": message_row[1],
                        "from_name": get_username_by_userid(conn, message_row[1]),
                        "content": message_row[3],
                        "content_type": message_row[4],
                        "content_time": message_row[5].strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
            return messages


def sendmessage(conn, token, chat_id, content, content_type):
    "Отправка сообщения пользователю"
    with conn.cursor() as cursor:
        user_id = get_userid_by_token(conn, token)
        if not check_user_membership(conn, user_id, chat_id):
            return "423"
        else:
            try:
                cursor.execute(
                    'INSERT INTO "messages" ("from_id", "chat_id", "content", "content_type") values (%(from_id)s, %(chat_id)s, %(content)s, %(content_type)s)',
                    {
                        "from_id": user_id,
                        "chat_id": chat_id,
                        "content": content,
                        "content_type": content_type,
                    },
                )
                conn.commit()
                return True
            except:
                return False


def register(conn, username, password, email):
    with conn.cursor() as cursor:
        try:
            cursor.execute(
                "insert into users (username, email, password) values (%(username)s, %(password)s, %(email)s);",
                {"username": username, "password": password, "email": email},
            )
            conn.commit()
            register_result = True
            token = cred_checker_with_token_generator(conn, username, password)[1]
        except psycopg2.errors.lookup(UNIQUE_VIOLATION) as e:
            register_result = False
            token = None
    return register_result, token


def fileds_check(msg_dict, fields_list=None):
    "Проверка наличия необходимых полей для работы. В случае отсутствия - будет возвращен HTTP 422"
    if type(msg_dict) != dict:
        return_msg = {
            "timestamp": get_current_date_str(),
            "status": "422",
            "error_msg": "Unsupported data",
        }
    else:
        if ["mode", "timestamp"] not in list(msg_dict.keys()):
            return_msg = {
                "timestamp": get_current_date_str(),
                "status": "422",
                "error_msg": "method or timestamp not provided",
            }
        elif fields_list not in list(msg_dict.keys()) and fields_list != None:
            return_msg = {
                "timestamp": get_current_date_str(),
                "status": "422",
                "error_msg": f'field(s) {", ".join(fields_list)} not provided',
            }
        else:
            return_msg = None

    return return_msg


def createpersonalchat(conn, token, contact_value, contact_mode):
    if contact_mode == "id":
        contact_id = contact_value
        user_id = get_userid_by_token(conn, token)
    elif contact_mode == "username":
        user_id = get_userid_by_token(conn, token)
        contact_id = get_userid_by_username(conn, contact_value)
    else:
        raise ValueError

    if None in [contact_id, user_id]:
        return ["409", ""]
    else:
        with conn.cursor() as cursor:
            cursor.execute(
                'INSERT INTO "chats" ("chat_name", "personal") values (%(chat_name)s, %(personal)s)',
                {
                    "chat_name": "personal",
                    "personal": True,
                },
            )

            # get chat_id
            cursor.execute('SELECT MAX(id) FROM chats;')
            chat_id = cursor.fetchone()[0]

            # insert data to chat_members table
            try:
                for i in [contact_id, user_id]:
                    cursor.execute(
                        'INSERT INTO "chat_members" ("chat_id", "user_id") values (%(chat_id)s, %(user_id)s)',
                        {"chat_id": chat_id, "user_id": i},
                    )
            except psycopg2.errors.lookup(FOREIGN_KEY_VIOLATION) as e:
                return ["409", ""]

            conn.commit()
        return ["200", chat_id]  # success


"""
Основная логика работы сервера

"""

app = Quart(__name__)


@app.websocket("/ws")
async def ws():
    await websocket.accept()
    while True:
        try:
            msg = await websocket.receive()
            conn = db_connector()  # подключаемся к БД
            msg_body = ast.literal_eval(msg)
            if fileds_check(msg_body) != None:
                await websocket.send(str(fileds_check(msg_body)))
            mode = msg_body["mode"]
            if mode == "auth":
                if fileds_check(msg_body, ["username", "password"]) != None:
                    await websocket.send(
                        str(fileds_check(msg_body, ["username", "password"]))
                    )
                # авторизация пользователя. успех - токен и 200, провал - None и 401
                cred_checker_result = cred_checker_with_token_generator(
                    conn, msg_body["username"], msg_body["password"]
                )  # проверяем авторизационные данные
                correct_cred = cred_checker_result[0]
                token = cred_checker_result[1]

                # формируем тело сообщения и отправляем тому, кто запросил
                new_msg_body = {
                    "mode": "auth",
                    "timestamp": get_current_date_str(),
                    "status": "200" if correct_cred else "401",
                    "token": token if correct_cred else None,
                }
                await websocket.send(str(new_msg_body))
            elif mode == "register":
                if fileds_check(msg_body, ["username", "password", "email"]) != None:
                    await websocket.send(
                        str(fileds_check(msg_body, ["username", "password", "email"]))
                    )

                register_result = register(
                    conn, msg_body["username"], msg_body["password"], msg_body["email"]
                )  # проверяем регистрационные данные
                register_status = register_result[0]
                token = register_result[1]

                # формируем тело сообщения и отправляем тому, кто запросил
                new_msg_body = {
                    "mode": "register",
                    "timestamp": get_current_date_str(),
                    "status": "200" if register_status else "409",
                    "token": token if register_status else None,
                }
                await websocket.send(str(new_msg_body))
            elif mode == "logout":
                if fileds_check(msg_body, ["token"]) != None:
                    await websocket.send(str(fileds_check(msg_body, ["token"])))
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
            elif mode == "getChats":
                if fileds_check(msg_body, ["token"]) != None:
                    await websocket.send(str(fileds_check(msg_body, ["token"])))
                if token_validation(conn, msg_body["token"]):
                    success = True
                    chats = getchats(conn, msg_body["token"])
                else:
                    success = False
                    chats = ""
                new_msg_body = {
                    "mode": "getChats",
                    "timestamp": get_current_date_str(),
                    "status": "200" if success else "401",
                    "chats": chats if success else None,
                }
                await websocket.send(str(new_msg_body))
            elif mode == "createPersonalChat":
                if (
                    fileds_check(msg_body, ["token", "contact_value", "contact_mode"])
                    != None
                ):
                    await websocket.send(
                        str(
                            fileds_check(
                                msg_body, ["token", "contact_value", "contact_mode"]
                            )
                        )
                    )
                if token_validation(conn, msg_body["token"]):
                    success = True
                    result = createpersonalchat(
                        conn,
                        msg_body["token"],
                        msg_body["contact_value"],
                        msg_body["contact_mode"],
                    )
                    result_code = result[0]
                    chat_id = result[1]
                else:
                    success = False
                    result_code = "401"
                    chat_id = ""
                new_msg_body = {
                    "mode": "createPersonalChat",
                    "timestamp": get_current_date_str(),
                    "status": result_code,
                    "chat_id": chat_id if result_code == "200" else None,
                }
                await websocket.send(str(new_msg_body))
            elif mode == "getMessages":
                if fileds_check(msg_body, ["token", "chat_id"]) != None:
                    await websocket.send(
                        str(fileds_check(msg_body, ["token", "chat_id"]))
                    )
                if token_validation(conn, msg_body["token"]):
                    success = True
                    messages = getmessages(conn, msg_body["token"], msg_body["chat_id"])
                    if messages == "423":
                        code = "423"
                        messages = ""
                    else:
                        code = "200"
                else:
                    success = False
                    code = 401
                    messages = ""
                new_msg_body = {
                    "mode": "getMessages",
                    "timestamp": get_current_date_str(),
                    "status": code,
                    "chats": messages if success else None,
                }
                await websocket.send(str(new_msg_body))
            elif mode == "sendMessage":
                if (
                    fileds_check(
                        msg_body, ["token", "chat_id", "content", "content_type"]
                    )
                    != None
                ):
                    await websocket.send(
                        str(
                            fileds_check(
                                msg_body,
                                ["token", "chat_id", "content", "content_type"],
                            )
                        )
                    )
                if token_validation(conn, msg_body["token"]):
                    success = sendmessage(
                        conn,
                        msg_body["token"],
                        msg_body["chat_id"],
                        msg_body["content"],
                        msg_body["content_type"],
                    )
                    if success == "423":
                        code = "423"
                    else:
                        code = "200"
                else:
                    code = "401"
                new_msg_body = {
                    "mode": "sendMessage",
                    "timestamp": get_current_date_str(),
                    "status": code,
                }
                await websocket.send(str(new_msg_body))
            else:
                await websocket.send(
                    str({"mode": mode, "timestamp": None, "status": "501"})
                )
        except AssertionError:
            await websocket.send(
                str({"mode": mode, "timestamp": None, "status": "403"})
            )
        except Exception as e:
            print(traceback.format_exc())
            return abort(500)


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
