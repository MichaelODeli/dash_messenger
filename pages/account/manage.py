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

register_page(
    __name__,
    path="/account/manage",
    icon="fa-solid:home",
    name="Управление аккаунтом | Dash Messenger",
)


def layout():

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
                                            className='tabs-content-colors'
                                        ),
                                        html.P(
                                            "Основные",
                                            className="fs-5 text-strong tabs-content-colors",
                                            style={'color': 'var(--bs-body-color)'},
                                        ),
                                    ],
                                    spacing='xs'
                                ),
                                value="main_tab",
                                className='p-2'
                            ),
                            dmc.Tab(
                                dmc.Group(
                                    [
                                        DashIconify(
                                            icon="material-symbols:privacy-tip",
                                            width=25,
                                            style={"color": "var(--bs-body-color)"},
                                            className='tabs-content-colors'
                                        ),
                                        html.P(
                                            "Приватность",
                                            className="fs-5 text-strong tabs-content-colors",
                                            style={'color': 'var(--bs-body-color)'}
                                        ),
                                    ],
                                    spacing='xs'
                                ),
                                value="privacy_tab",
                                className='p-2'
                            ),
                            dmc.Tab(
                                dmc.Group(
                                    [
                                        DashIconify(
                                            icon="material-symbols:help-rounded",
                                            width=25,
                                            style={"color": "var(--bs-body-color)"},
                                            className='tabs-content-colors'
                                        ),
                                        html.P(
                                            "Справочный центр",
                                            className="fs-5 text-strong tabs-content-colors",
                                            style={'color': 'var(--bs-body-color)'}
                                        ),
                                    ],
                                    spacing='xs'
                                ),
                                value="help_tab",
                                className='p-2'
                            ),
                        ],
                        grow=True
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            ["Основные"],
                            className="border border-top-0 h-100 p-3 custom-border-color",
                        ),
                        value="main_tab",
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            ["Приватность"],
                            className="border border-top-0 h-100 p-3 custom-border-color",
                        ),
                        value="privacy_tab",
                    ),
                    dmc.TabsPanel(
                        html.Div(
                            ["Справочный центр"],
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
