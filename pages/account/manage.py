"Восстановление пароля."

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

register_page(
    __name__,
    path="/account/manage",
    icon="fa-solid:home",
    name="Управление аккаунтом | Dash Messenger",
)


def get_form_floating(label, id, placeholder, itype="text", value=None, disabled=False):
    return dbc.FormFloating(
        [
            dbc.Input(
                type=itype,
                placeholder=placeholder,
                value=value,
                disabled=disabled,
                id=id,
            ),
            dbc.Label(label),
        ],
        class_name="w-100",
    )


def layout():

    main_tab = dmc.Stack(
        [
            html.H5("Основные настройки аккаунта"),
            dmc.Grid(
                [
                    dmc.GridCol(
                        [
                            dbc.Card(
                                dmc.Stack(
                                    [
                                        html.H5("Данные аккаунта"),
                                        get_form_floating(
                                            "Адрес электронной почты",
                                            "lk-email",
                                            "Эл. почта",
                                            "email",
                                            disabled=True,
                                            value="dan***@gmail.com",
                                        ),
                                        get_form_floating(
                                            "Никнейм",
                                            "lk-nickname",
                                            "Введите новый никнейм",
                                            "text",
                                            value="MichaelODeli",
                                            disabled=True,
                                        ),
                                        # dbc.Button('Как мне изменить эти данные?', class_name='ps-5 pe-5'),
                                        dmc.Space(h=10),
                                        html.H5("Изменение пароля"),
                                        get_form_floating(
                                            "Старый пароль",
                                            "old-password-change",
                                            "Введите старый пароль",
                                            "password",
                                        ),
                                        get_form_floating(
                                            "Новый пароль",
                                            "new-password-change",
                                            "Введите новый пароль",
                                            "password",
                                        ),
                                        get_form_floating(
                                            "Повторите новый пароль",
                                            "retype-new-password-change",
                                            "Повторите ввод нового пароль",
                                            "password",
                                        ),
                                        dbc.Button(
                                            "Изменить пароль", class_name="ps-5 pe-5"
                                        ),
                                    ],
                                    align="center",
                                    gap="xs",
                                ),
                                class_name="h-100 w-100 p-3",
                            )
                        ],
                        span=8,
                        className="adaptive-width",
                    ),
                ],
                w="100%",
                justify='center'
            ),
        ],
        className="w-100",
        align="center",
    )

    privacy_tab = dmc.Stack(
        [
            html.H5("Приватность"),
            dmc.Grid(
                [
                    dmc.GridCol(
                        [
                            dbc.Card(
                                dmc.Stack(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label("Кто может писать мне сообщения?", html_for="form1"),
                                                dbc.Select(
                                                    id="form1",
                                                    options=[
                                                        {"label": "Все пользователи", "value": "all"},
                                                        {"label": "Только мои контакты", "value": "only_contacts"},
                                                    ],
                                                    value='all'
                                                )
                                            ],
                                            className="mb-3",
                                        ),
                                        html.Div(
                                            [
                                                dbc.Label("Кто может найти меня по нику?", html_for="form2"),
                                                dbc.Select(
                                                    id="form2",
                                                    options=[
                                                        {"label": "Все пользователи", "value": "all"},
                                                        {"label": "Контакты контактов", "value": "only_contacts"},
                                                        {"label": "Никто", "value": "nobody"},
                                                    ],
                                                    value='all'
                                                )
                                            ],
                                            className="mb-3",
                                        ),
                                        dbc.Button('Сохранить изменения')
                                    ],
                                    align="center",
                                    gap="xs",
                                ),
                                class_name="h-100 w-100 p-3",
                            )
                        ],
                        span=8,
                        className="adaptive-width",
                    ),
                ],
                w="100%",
                justify='center'
            ),
        ],
        className="w-100",
        align="center",
    )
    help_tab = html.Div("Справочный центр")

    return dmc.Stack(
        [
            html.H4("Управление аккаунтом"),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab(
                                dmc.Group(
                                    [
                                        DashIconify(
                                            icon="material-symbols:account-circle",
                                            width=25,
                                            style={"color": "var(--bs-body-color)"},
                                            className="tabs-content-colors",
                                        ),
                                        html.P(
                                            "Основные",
                                            className="fs-6 text-strong tabs-content-colors adaptive-hide",
                                            style={"color": "var(--bs-body-color)"},
                                        ),
                                    ],
                                    gap="xs",
                                ),
                                value="main_tab",
                                className="p-2 manage-tab",
                            ),
                            dmc.TabsTab(
                                dmc.Group(
                                    [
                                        DashIconify(
                                            icon="material-symbols:privacy-tip",
                                            width=25,
                                            style={"color": "var(--bs-body-color)"},
                                            className="tabs-content-colors",
                                        ),
                                        html.P(
                                            "Приватность",
                                            className="fs-6 text-strong tabs-content-colors adaptive-hide",
                                            style={"color": "var(--bs-body-color)"},
                                        ),
                                    ],
                                    gap="xs",
                                ),
                                value="privacy_tab",
                                className="p-2 manage-tab",
                                # disabled=True
                            ),
                            dmc.TabsTab(
                                dmc.Group(
                                    [
                                        DashIconify(
                                            icon="material-symbols:help-rounded",
                                            width=25,
                                            style={"color": "var(--bs-body-color)"},
                                            className="tabs-content-colors",
                                        ),
                                        html.P(
                                            "Справочный центр",
                                            className="fs-6 text-strong tabs-content-colors adaptive-hide",
                                            style={"color": "var(--bs-body-color)"},
                                        ),
                                    ],
                                    gap="xs",
                                ),
                                value="help_tab",
                                className="p-2 manage-tab",
                                disabled=True
                            ),
                        ],
                        # grow=True,
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            main_tab,
                            className="border border hmin-100 p-3 custom-border-color",
                        ),
                        value="main_tab",
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            privacy_tab,
                            className="border border hmin-100 p-3 custom-border-color",
                        ),
                        value="privacy_tab",
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            help_tab,
                            className="border border hmin-100 p-3 custom-border-color",
                        ),
                        value="help_tab",
                    ),
                ],
                orientation="vertical",
                variant="pills",
                w="100%",
                h="100%",
                value="main_tab",
            ),
        ],
        align="center",
        # justify="center",
        h="100%",
        pt="3vh",
        w="100%",
    )