from quart import websocket, Quart, abort
import ast
import datetime
import psycopg2
import uuid

app = Quart(__name__)


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
    # return_res = ''
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


@app.websocket("/ws")
async def ws():
    await websocket.accept()
    while True:
        msg = await websocket.receive()
        try:
            conn = db_connector() # подключаемся к БД
            msg_body = ast.literal_eval(msg)
            mode = msg_body["mode"]
            print(mode)
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
                print(msg_body)
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
                pass
            else:
                await websocket.send(
                    str(
                        {"mode": mode, "timestamp": None, "status": "501"}
                    )  # not implemented
                )
        except Exception as e:
            print(e)
            return abort(500)


if __name__ == "__main__":
    app.run(port=5000)
