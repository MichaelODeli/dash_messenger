"Главное окно мессенджера"

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
    clientside_callback,
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash_extensions import DeferScript
import random

register_page(
    __name__,
    path="/im",
    icon="fa-solid:home",
    name="Dash Messenger",
)


def get_icon(icon_name, width):
    return DashIconify(
        icon=icon_name,
        width=width,
    )


def get_leftside_contacts(
    nickname,
    msg_text,
    msg_time="00:00",
    active=False,
    user_icon="/assets/user_icon.png",
):
    active_background = " selected-tr" if active else ""
    return html.Tr(
        [
            html.Td(html.Img(src=user_icon, className="transp-back user-icon")),
            html.Td(
                html.Div(
                    [
                        html.Strong(nickname),
                        html.Br(),
                        html.P(msg_text),
                        html.P(msg_time, className="leftside-message-time"),
                    ],
                    className="leftside-msg-text transp-back",
                ),
                className="w-100",
            ),
        ],
        className="tr-hover border-bottom w-100 leftside-msg" + active_background,
        style={"margin": "10px"},
        id={"type": f"contacts-tab", "index": nickname},
    )


def get_message_tr(
    nickname, message_content, msg_time="00:00", user_icon="/assets/user_icon.png"
):
    return dmc.TableTr(
        [
            dmc.TableTd(
                [
                    html.Img(
                        src=user_icon,
                        className="transp-back user-icon",
                        style={"height": "32px"},
                    )
                ],
                className="d-flex p-3",
                style={"width": "fit-content"},
            ),
            dmc.TableTd(
                dmc.Stack(
                    [html.Strong(nickname), message_content],
                    gap="xs",
                ),
                className="pb-2 pt-1 w-100",
            ),
            dmc.TableTd(
                [
                    html.P(
                        msg_time, style={"color": "var(--bs-secondary-text-emphasis)"}
                    )
                ],
                className="p-2 h-100",
                style={"width": "fit-content", "vertical-align": "top"},
            ),
        ],
        className="tr-hover",
    )


def layout():
    chats_threedots_menu = dbc.Popover(
        dbc.ButtonGroup(
            [
                dbc.Button("Создать беседу", color="primary", outline=True),
                dbc.Button("Добавить контакт", color="primary", outline=True),
            ],
            vertical=True,
            class_name="w-100",
        ),
        body=True,
        target="chats-threedots-menu-open",
        trigger="hover",
        placement="bottom",
        id="popover",
    )

    contacts = dmc.Stack(
        [
            dmc.Grid(
                [
                    dmc.GridCol(
                        html.H5("Список чатов", className="text-center"), span="auto"
                    ),
                    dmc.GridCol(
                        [
                            chats_threedots_menu,
                            dbc.Button(
                                get_icon(
                                    icon_name="mdi:dots-horizontal",
                                    width=25,
                                ),
                                outline=True,
                                color="primary",
                                # style={"padding": "var(--bs-btn-padding-y)"},
                                id="chats-threedots-menu-open",
                                class_name="p-1 adaptive-hide",
                            ),
                        ],
                        span="content",
                    ),
                ],
            ),
            dmc.ScrollArea(
                dbc.Table(
                    [
                        get_leftside_contacts(
                            "MotherOfGod", "Иди кушать уже", active=True
                        )
                    ]
                    + [
                        get_leftside_contacts(
                            f"SuperDuper{i}23", "Ну как там с деньгами?"
                        )
                        for i in range(20)
                    ],
                    className="w-100 pe-1 mb-0",
                    hover=True,
                ),
                mah="100%",
                type="auto",
                m="auto",
                w="100%",
                offsetScrollbars=True,
                className="dynamic-scroll-height border-start",
            ),
        ],
        w="100%",
        m="auto",
        gap=0,
    )

    text_input_bar = dmc.Group(
        [
            dbc.InputGroup(
                [
                    DeferScript(src="/assets/scroll.js"),
                    dbc.Input(placeholder="Cообщение", id="message-text"),
                    dbc.Button(get_icon("mdi:paperclip", width=20), disabled=True),
                    dbc.Button(get_icon("bx:smile", width=20), disabled=True),
                    dbc.Button(get_icon("mdi:send", width=20), id="send-message"),
                ],
            ),
            dbc.Button(
                get_icon("mdi:arrow-down", width=20),
                # disabled=True,
                id="downClick",
                class_name="downClick",
            ),
        ],
        style={'flex-wrap': 'nowrap'}
    )

    msg_threedots_menu = dbc.Popover(
        dbc.ButtonGroup(
            [
                dbc.Button(
                    "Отключить уведомления",
                    color="primary",
                    outline=True,
                    id="messenger-toggle-notif",
                ),
                dbc.Button(
                    "Удалить чат",
                    color="danger",
                    outline=True,
                    id="messenger-delete-chat",
                ),
                dbc.Button(
                    "Заблокировать", color="danger", outline=True, id="messenger-ban"
                ),
            ],
            vertical=True,
            class_name="w-100",
        ),
        body=True,
        target="msg-threedots-menu-open",
        trigger="hover",
        placement="bottom",
        id="popover",
    )

    messages = dmc.Stack(
        [
            html.Div(
                dmc.Grid(
                    [
                        dmc.GridCol(
                            dbc.Button(
                                get_icon(
                                    icon_name="material-symbols:menu-rounded",
                                    width=25,
                                ),
                                outline=True,
                                color="primary",
                                # style={"padding": "var(--bs-btn-padding-y)"},
                                id="open-contacts-drawer",
                                class_name="p-1",
                            ),
                            span="content",
                            className="adaptive-show",
                        ),
                        dmc.GridCol(
                            dmc.Group(
                                [
                                    html.Img(
                                        src="/assets/user_icon.png",
                                        className="transp-back user-icon",
                                        style={"height": "32px"},
                                    ),
                                    html.H5("MotherOfGod", className="m-0"),
                                ]
                            ),
                            span="auto",
                            className="ms-2",
                        ),
                        dmc.GridCol(
                            [
                                dbc.Button(
                                    get_icon(
                                        icon_name="mdi:dots-horizontal",
                                        width=25,
                                    ),
                                    outline=True,
                                    color="primary",
                                    # style={"padding": "var(--bs-btn-padding-y)"},
                                    id="msg-threedots-menu-open",
                                    class_name="p-1",
                                ),
                                msg_threedots_menu,
                            ],
                            span="content",
                        ),
                    ],
                    gutter="xs",
                ),
                className="w-100 roww fit-content border rounded-top-1",
            ),
            html.Div(
                dmc.ScrollArea(
                    [
                        dmc.Table(
                            [
                                get_message_tr(
                                    "MotherOfGod", html.P("Иди кушать уже!")
                                ),
                                get_message_tr("Вы", html.P("Да щас, иду уже!")),
                            ]
                            * 15,
                            className="w-100 pe-1 mb-0 cover",
                            highlightOnHover=True,
                            striped=False,
                            id="messages-table",
                        )
                    ],
                    type="auto",
                    offsetScrollbars=True,
                    className="h-100 w-100 msg_table",
                ),
                className="w-100 roww fill-remain border border-top-0 rounded-bottom-1 mb-2",
            ),
            html.Div(
                text_input_bar,
                className="w-100 roww fit-content",
            ),
        ],
        w="100%",
        # h='90%',
        className="boxx",
        gap=0,
    )

    return dmc.Stack(
        [
            dmc.Drawer(
                dmc.Stack(
                    [
                        # dbc.Alert(
                        #     "Редактирование списка чатов доступно только с ПК",
                        #     color="warning",
                        #     class_name='m-0'
                        # ),
                        contacts,
                    ],
                    className="w-100",
                    gap=0,
                ),
                title=html.H5("Список контактов"),
                id="drawer-contacts",
                padding="md",
                zIndex=10,
                size="90%",
            ),
            dmc.Grid(
                [
                    dmc.GridCol(
                        contacts,
                        span=3,
                        mih="100%",
                        p=0,
                        className="d-flex adaptive-hide",  # temp
                    ),
                    dmc.GridCol(
                        messages,
                        span=9,
                        style={
                            "margin-bottom": "auto !important",
                        },
                        h="100%",
                        className=" adaptive-width mt-0 p-0 mb-auto",
                    ),
                ],
                w="100%",
                h="100%",
                # className="border",
                m="auto",
            ),
        ],
        miw="100%",
        h="100%",
        justify="center",
    )


@callback(
    Output("MotherOfGod", "n_clicks"),
    Input("MotherOfGod", "n_clicks"),
    prevent_inital_call=True,
)
def click_handle(n_clicks):
    # print('Clicked on row')
    return 0


@callback(
    Output("drawer-contacts", "opened"),
    Input("open-contacts-drawer", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_contacts(n_clicks):
    return True


@callback(
    Output("popover", "is_open"),
    [
        Input("messenger-toggle-notif", "n_clicks"),
        Input("messenger-ban", "n_clicks"),
        Input("messenger-delete-chat", "n_clicks"),
    ],
    [State("popover", "is_open")],
)
def toggle_popover(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open
