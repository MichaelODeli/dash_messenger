"Восстановление пароля."
"Если пользователь не авторизован - показываем форму восстановления"
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

register_page(__name__, path="/auth/recovery", icon="fa-solid:home", name="Восстановление | Dash Messenger")


def layout():
    nickname_input = html.Div(
        [
            dbc.Input(type="text", id="recovery-nickname", placeholder="Введите nickname"),
        ],
        className="mb-3 pt-3",
    )

    email_input = html.Div(
        [
            dbc.Input(type="email", id="recovery-email", placeholder="Введите email"),
        ],
        className="mb-3 pt-3",
    )

    return dmc.Stack(
                [
                    dbc.Form(
                        [
                            html.H4('Восстановление аккаунта', className='pb-4'),
                            html.P('Какие данные от аккаунта Вы помните?', className='text-center pb-1'),
                            dbc.Tabs(
                                [
                                    dbc.Tab(email_input, label="Я помню почту", tab_id='tab-1'),
                                    dbc.Tab(nickname_input, label="Я помню никнейм", tab_id='tab-2'),
                                ],
                                active_tab="tab-1",
                            ),
                            dbc.Button(
                                "Восстановить аккаунт",
                                style={"width": "100%"},
                                id='btn-recovery-account'
                            ),
                            dmc.Space(h=5),
                            html.A(
                                "Я вспомнил данные!",
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
