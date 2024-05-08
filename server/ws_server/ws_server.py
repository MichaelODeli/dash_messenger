from quart import websocket, Quart, abort
import ast
import random
import psycopg2

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


def cred_checker(conn, username, password):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM users WHERE username=%(username)s and password=%(password)s;",
            {"username": username, "password": password},
        )
        result = cursor.fetchone()
        if result != None:
            user_exist = True
            user_id = result[0]
            token = str(random.randint(100000, 999999))
            cursor.execute(
                'INSERT INTO "tokens" ("token", "user_id", "status", "valid_until") values (%(token)s, %(user_id)s, %(status)s, %(valid_until)s)',
                {
                    "token": token,
                    "user_id": user_id,
                    "status": "given",
                    "valid_until": "2099-01-08 04:05:06",
                },
            )
            conn.commit()
        else:
            user_exist = False
            token = None
    return user_exist, token


@app.websocket("/ws")
async def ws():
    await websocket.accept()
    while True:
        msg = await websocket.receive()
        try:
            msg_body = ast.literal_eval(msg)
            mode = msg_body["mode"]
            if mode == "auth":
                # авторизация пользователя. успех - токен и 200, провал - None и 401
                conn = db_connector() # подключаемся к БД
                cred_checker_result = cred_checker(
                    conn, msg_body["username"], msg_body["password"]
                ) # проверяем авторизационные данные
                correct_cred = cred_checker_result[0]
                token = cred_checker_result[1]
                conn.close()

                # формируем тело сообщения и отправляем тому, кто запросил
                new_msg_body = {
                    "mode": "auth",
                    "timestamp": None,
                    "status": "200" if correct_cred else "401",
                    "token": (token if correct_cred else None),
                }

                await websocket.send(str(new_msg_body))
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
