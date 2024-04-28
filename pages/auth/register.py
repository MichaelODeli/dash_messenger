"Регистрация."
"Если пользователь не авторизован - показываем форму регистрации"
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

register_page(__name__, path="/auth/register", icon="fa-solid:home", name="Регистрация | Dash Messenger")


def layout():
    nickname_input = html.Div(
        [
            dbc.Label("Никнейм", html_for="register-nickname"),
            dbc.Input(type="text", id="register-nickname", placeholder="Введите nickname"),
        ],
        className="mb-3",
    )

    email_input = html.Div(
        [
            dbc.Label("Электронная почта", html_for="register-email"),
            dbc.Input(type="email", id="register-email", placeholder="Введите email"),
        ],
        className="mb-3",
    )

    password_input = html.Div(
        [
            dbc.Label("Пароль", html_for="register-password"),
            dbc.Input(
                type="password",
                id="register-password",
                placeholder="Введите пароль",
            ),
        ],
        className="mb-3",
    )

    retype_password_input = html.Div(
        [
            dbc.Label("Повторите пароль", html_for="register-password-retype"),
            dbc.Input(
                type="password",
                id="register-password-retype",
                placeholder="Повторите ввод пароля",
            ),
        ],
        className="mb-3",
    )

    return dmc.Stack(
                [
                    dbc.Form(
                        [
                            html.H4('Регистрация аккаунта', className='pb-4'),
                            nickname_input,
                            email_input,
                            password_input,
                            retype_password_input,
                            dbc.Button(
                                "Создать аккаунт",
                                style={"width": "100%"},
                                id='btn-create-account'
                            ),
                            dmc.Space(h=5),
                            html.A(
                                "У меня уже есть аккаунт",
                                style={"width": "100%"},
                                className='btn btn-primary',
                                href='/'
                            ),
                        ],
                        class_name='border rounded p-3'
                    )
                ],
                style={"width": "100%"},
                align='center',
                justify='center',
                h='100%',
                # pt='5vh',
                w='100%',
            )
