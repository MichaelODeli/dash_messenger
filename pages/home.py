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
from dash_iconify import DashIconify

register_page(__name__, path="/", icon="fa-solid:home", name="Главная | Dash Messenger")


def layout():
    email_input = html.Div(
        [
            dbc.Label("Электронная почта", html_for="example-email"),
            dbc.Input(type="email", id="auth-email", placeholder="Введите email"),
        ],
        className="mb-3",
    )

    password_input = html.Div(
        [
            dbc.Label("Пароль", html_for="example-password"),
            dbc.Input(
                type="password",
                id="auth-password",
                placeholder="Введите пароль",
            ),
        ],
        className="mb-3",
    )

    return dmc.Stack(
        [
            dmc.Grid(
                [
                    dmc.GridCol(
                        [
                            dbc.Card(
                                [html.P("Блок с полезной информацией", className="text-center", style={'margin': 'auto'})],
                                style={"width": "100%", "height": "100%"},
                            )
                        ],
                        span=6,
                        className="adaptive-hide h-100",
                    ),
                    dmc.GridCol(
                        [
                            dmc.Stack(
                                [
                                    dbc.Card(
                                        [
                                            html.H4(
                                                "Dash Messenger",
                                                className="text-center pb-1",
                                            ),
                                            html.H5(
                                                "Основан на технологии WebSocket",
                                                className="text-center pb-2",
                                            ),
                                            dmc.Space(h=10),
                                            dbc.Form(
                                                [
                                                    email_input,
                                                    password_input,
                                                    dbc.Button(
                                                        "Войти в аккаунт",
                                                        style={"width": "100%"},
                                                    ),
                                                ],
                                                style={
                                                    "width": "65%",
                                                    "margin": "auto",
                                                },
                                                class_name="adaptive-input-width",
                                            ),
                                        ],
                                        style={"width": "100%", "padding": "20px"},
                                    ),
                                    dbc.Card(
                                        dmc.Stack(
                                            [
                                                html.H5(
                                                    "Нет аккаунта или забыли пароль?",
                                                    className="text-center",
                                                ),
                                                html.A(
                                                    "Создать аккаунт",
                                                    style={"width": "content"},
                                                    href="/auth/register",
                                                    className="btn btn-primary",
                                                ),
                                                html.A(
                                                    "Восстановить пароль",
                                                    style={"width": "content"},
                                                    href="/auth/recovery",
                                                    className="btn btn-primary",
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        style={"width": "100%", "padding": "20px"},
                                    ),
                                ]
                            )
                        ],
                        span=6,
                        className="adaptive-width",
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
