"Домашняя страница."
"Если пользователь не авторизован - показываем форму авторизации"
"Если пользователь авторизован - перенаправляем его на страницу '/messenger/im'"

from dash import (
    dcc,
    html,
    Input,
    Output,
    callback,
    register_page,
    State,
    Input,
    Output,
    no_update,
    ALL,
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from controllers.utils import get_current_date_str
from flask import request as flask_request
import ast
import requests


register_page(__name__, path="/", icon="fa-solid:home", name="Главная | Dash Messenger")


def layout():
    print("------- loaded home page -------")
    secret_fields = html.Div(
        [
            html.Div(id="hidden_div_for_redirect_callback_auth"),
            dcc.Interval(
                id="load_interval_auth",
                n_intervals=0,
                max_intervals=0,  # <-- only run once
                interval=1,
            ),
        ]
    )

    email_input = html.Div(
        [
            # dbc.Label("Имя пользователя", html_for="auth-username"),
            dbc.Input(type="text", id="auth-username", placeholder="Имя пользователя"),
        ],
        className="mb-3",
    )

    password_input = html.Div(
        [
            # dbc.Label("Пароль", html_for="auth-password"),
            dbc.Input(
                type="password",
                id="auth-password",
                placeholder="Пароль",
            ),
        ],
        className="mb-3",
    )

    return dmc.Stack(
        [
            secret_fields,
            dmc.Grid(
                [
                    dmc.GridCol(
                        [
                            dbc.Card(
                                [
                                    html.P(
                                        "Блок с полезной информацией и описанием проекта",
                                        className="text-center",
                                        style={"margin": "auto"},
                                    )
                                ],
                                style={"width": "100%", "min-height": "50vh"},
                                class_name="h-100",
                            )
                        ],
                        span=7,
                        className="adaptive-hide h-100",
                    ),
                    dmc.GridCol(
                        [
                            dmc.Stack(
                                [
                                    dbc.Card(
                                        [
                                            dmc.LoadingOverlay(
                                                visible=True,
                                                id="loading-overlay",
                                                zIndex=1000,
                                                overlayProps={
                                                    "radius": "sm",
                                                    "blur": 2,
                                                },
                                            ),
                                            html.H4(
                                                "Dash Messenger",
                                                className="text-center pb-1",
                                            ),
                                            html.H5(
                                                "Основан на технологии WebSocket",
                                                className="text-center pb-2",
                                            ),
                                            dmc.Space(h=10),
                                            html.Div(
                                                [
                                                    email_input,
                                                    password_input,
                                                    dbc.Button(
                                                        "Войти в аккаунт",
                                                        style={"width": "100%"},
                                                        id="auth-btn-trigger",
                                                    ),
                                                    dmc.Grid(
                                                        [
                                                            dmc.GridCol(
                                                                html.A(
                                                                    "Создать аккаунт",
                                                                    style={
                                                                        "width": "content"
                                                                    },
                                                                    href="/auth/register",
                                                                    className="disabled link-underline link-underline-opacity-0",
                                                                ),
                                                                span="content",
                                                                className="ps-0",
                                                            ),
                                                            dmc.GridCol(
                                                                "", span="auto"
                                                            ),
                                                            dmc.GridCol(
                                                                html.A(
                                                                    "Забыли пароль?",
                                                                    style={
                                                                        "width": "content",
                                                                    },
                                                                    href="/auth/recovery",
                                                                    className="link-underline link-underline-opacity-0",
                                                                ),
                                                                span="content",
                                                                className="pe-0",
                                                            ),
                                                        ],
                                                        style={"display": "none"},
                                                    ),
                                                ],
                                                style={
                                                    "width": "75%",
                                                    "margin-left": "auto",
                                                    "margin-right": "auto",
                                                },
                                                className="adaptive-input-width",
                                                id="input_form",
                                            ),
                                        ],
                                        style={
                                            "width": "100%",
                                            "padding": "20px",
                                            "display": "flex",
                                            "justify-content": "center",
                                        },
                                        class_name="h-100",
                                    ),
                                ],
                                className="h-100 m-auto",
                                justify="center",
                            )
                        ],
                        span=5,
                        className="adaptive-width h-100",
                    ),
                ],
                style={"width": "100%"},
            ),
        ],
        align="center",
        justify="center",
        h="100%",
        # pt="10vh",
    )


# auth - send data
@callback(
    Output("ws", "send", allow_duplicate=True),
    Output("auth-username", "invalid", allow_duplicate=True),
    Output("auth-password", "invalid", allow_duplicate=True),
    Input("auth-btn-trigger", "n_clicks"),
    State("auth-username", "value"),
    State("auth-password", "value"),
    prevent_initial_call=True,
)
def make_auth(n_clicks, username, password):
    if None in [username, password] and n_clicks != None:
        # return [no_update] * 3
        return (
            no_update,
            True if username == None else no_update,
            True if password == None else no_update,
        )
    elif n_clicks == None:
        return [no_update] * 3
    else:
        message_structure = {
            "mode": "auth",
            "timestamp": get_current_date_str(),
            "username": username,
            "password": password,
        }
        return str(message_structure), no_update, no_update


# auth - read data
@callback(
    Output("token-store", "data"),
    Output("auth-username", "invalid"),
    Output("auth-password", "invalid"),
    Output("hidden_div_for_redirect_callback_auth", "children", allow_duplicate=True),
    Output("header-btn-logout", "style", allow_duplicate=True),
    Input("ws", "message"),
    prevent_initial_call=True,
)
def read_auth_data(message):
    if message != None:
        msg_data = ast.literal_eval(message["data"])
        print(msg_data)
        if msg_data["mode"] == "auth" and msg_data["status"] == "200":
            print("received token", msg_data["token"])
            return (
                msg_data["token"],
                no_update,
                no_update,
                dcc.Location(pathname="/im", id="someid_doesnt_matter_auth"),
                {"display": "unset"},
            )
        elif msg_data["mode"] == "auth" and msg_data["status"] == "401":
            return None, True, True, no_update, no_update
        else:
            return [no_update] * 5


# redirector if token in store and if token valid
@callback(
    Output("hidden_div_for_redirect_callback_auth", "children"),
    Output("header-btn-logout", "style"),
    Input("load_interval_auth", "n_intervals"),
    State("token-store", "data"),
    running=[
        (Output("loading-overlay", "visible"), True, False),
    ],
)
def redirector(n_intervals, token):
    hostname = flask_request.headers.get("Host").split(":")[0]
    print("stored token", token)
    if token != None:
        response = requests.get(
            f"http://{hostname}:5000/api",
            headers={"Authorization": token, "Sec-Fetch-Mode": "token_validation"},
        )
        token_test_result = response.content.decode("utf-8")
        if token_test_result == "True":
            print("user redirected to messenger page")
            return dcc.Location(pathname="/im", id="someid_doesnt_matter_auth"), None
        else:
            print("user redirected to home page (invalid stored token)")
            return no_update, None
    else:
        return no_update, no_update
