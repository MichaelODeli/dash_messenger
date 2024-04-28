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
            html.H4("Основные настройки аккаунта"),
            dmc.Grid(
                [
                    dmc.Col(
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
                                    spacing="xs",
                                ),
                                class_name="h-100 w-100 p-3",
                            )
                        ],
                        span=6,
                        className="adaptive-width",
                    ),
                    # dmc.Col(
                    #     [
                    #         dbc.Card(
                    #             dmc.Stack(
                    #                 [html.H5("Смена пароля аккаунта")], align="center"
                    #             ),
                    #             class_name="h-100 w-100 p-3",
                    #         )
                    #     ],
                    #     span=6,
                    #     className="adaptive-width",
                    # ),
                ],
                w="100%",
                justify='center'
            ),
        ],
        className="w-100",
        align="center",
    )
    privacy_tab = html.Div("Приватность")
    help_tab = html.Div("Справочный центр")

    return dmc.Stack(
        [
            html.H4("Управление аккаунтом"),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab(
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
                                            className="fs-5 text-strong tabs-content-colors",
                                            style={"color": "var(--bs-body-color)"},
                                        ),
                                    ],
                                    spacing="xs",
                                ),
                                value="main_tab",
                                className="p-2",
                            ),
                            dmc.Tab(
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
                                            className="fs-5 text-strong tabs-content-colors",
                                            style={"color": "var(--bs-body-color)"},
                                        ),
                                    ],
                                    spacing="xs",
                                ),
                                value="privacy_tab",
                                className="p-2",
                                disabled=True
                            ),
                            dmc.Tab(
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
                                            className="fs-5 text-strong tabs-content-colors",
                                            style={"color": "var(--bs-body-color)"},
                                        ),
                                    ],
                                    spacing="xs",
                                ),
                                value="help_tab",
                                className="p-2",
                                disabled=True
                            ),
                        ],
                        grow=True,
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            main_tab,
                            className="border border-top-0 h-100 p-3 custom-border-color",
                        ),
                        value="main_tab",
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            privacy_tab,
                            className="border border-top-0 h-100 p-3 custom-border-color",
                        ),
                        value="privacy_tab",
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            help_tab,
                            className="border border-top-0 h-100 p-3 custom-border-color",
                        ),
                        value="help_tab",
                    ),
                ],
                orientation="horizontal",
                variant="outline",
                w="100%",
                h="100%",
                value="main_tab",
            ),
        ],
        align="center",
        justify="center",
        h="100%",
        pt="5vh",
        w="100%",
    )