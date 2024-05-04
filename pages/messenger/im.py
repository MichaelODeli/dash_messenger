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
from pages.messenger import im_modals

register_page(
    __name__,
    path="/im",
    icon="fa-solid:home",
    name="Dash Messenger",
)


def get_icon(icon_name, width, style=None):
    return DashIconify(icon=icon_name, width=width, style=style)


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
    modals = html.Div(
        [
            im_modals.messenger_modal_addcontact(),
            im_modals.messenger_modal_deletechat()
        ]
    )

    chats_threedots_menu = dmc.HoverCard(
        position="bottom",
        withArrow=True,
        width=200,
        shadow="md",
        children=[
            dmc.HoverCardTarget(
                dbc.Button(
                    get_icon(
                        icon_name="mdi:dots-horizontal",
                        width=25,
                    ),
                    outline=True,
                    color="primary",
                    id="messenger-btn-contacts_actions",
                    class_name="p-1",
                ),
            ),
            dmc.HoverCardDropdown(
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Создать беседу",
                            color="primary",
                            outline=True,
                            id="messenger-btn-create_chat",
                            disabled=True
                        ),
                        dbc.Button(
                            "Добавить контакт",
                            color="primary",
                            outline=True,
                            id="messenger-btn-add_contact",
                        ),
                    ],
                    vertical=True,
                    class_name="w-100",
                ),
            ),
        ],
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
                    id="messenger-table-contacts",
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

    attachment_bar = dmc.HoverCard(
        disabled=True,
        closeDelay=300,
        position="top",
        withArrow=True,
        width=400,
        shadow="md",
        children=[
            dmc.HoverCardTarget(
                dbc.Button(
                    get_icon("mdi:paperclip", width=20),
                    class_name="adaptive-hide no-rounded",
                    id="messenger-btn-attachment_actions",
                    disabled=True
                )
            ),
            dmc.HoverCardDropdown(
                dmc.Tabs(
                    [
                        dmc.TabsPanel(
                            dmc.Stack(
                                [
                                    # html.H5("Стикеры", className='text-center pb-2'),
                                    html.Div(
                                        dbc.Table(
                                            [
                                                html.Tr(
                                                    [
                                                        html.Td(
                                                            html.Center(
                                                                html.Img(
                                                                    src="/assets/user_icon.png",
                                                                    style={
                                                                        "height": "50px"
                                                                    },
                                                                    className="pt-1 pb-1",
                                                                )
                                                            ),
                                                            className="tr-hover",
                                                        )
                                                    ]
                                                    * 4
                                                )
                                            ]
                                            * 7,
                                            style={"box-shadow": "unset"},
                                            class_name="background-0",
                                            id="messenger-table-stickers",
                                        ),
                                        style={
                                            "max-height": "290px",
                                            "overflow-y": "auto",
                                            "margin": "auto",
                                            "width": "100%",
                                        },
                                    )
                                ],
                                justify="center",
                            ),
                            value="stickers",
                            className="border border-bottom-0 p-2",
                            h=300,
                        ),
                        dmc.TabsPanel(
                            dmc.Stack(
                                [
                                    dbc.ButtonGroup(
                                        [
                                            dbc.Button(
                                                "Отправить фото",
                                                color="primary",
                                                outline=True,
                                                id="messenger-btn-attachment_photo",
                                            ),
                                            dbc.Button(
                                                "Отправить видео",
                                                color="primary",
                                                outline=True,
                                                id="messenger-btn-attachment_video",
                                            ),
                                            dbc.Button(
                                                "Отправить файл",
                                                color="primary",
                                                outline=True,
                                                id="messenger-btn-attachment_file",
                                            ),
                                        ],
                                        vertical=True,
                                        class_name="w-100 m-auto d-flex",
                                    ),
                                ],
                                justify="center",
                                className="d-flex w-100 h-100",
                            ),
                            value="attachments",
                            className="border border-bottom-0 p-2",
                            h=300,
                        ),
                        dmc.TabsList(
                            [
                                dmc.TabsTab(
                                    get_icon("mdi:paperclip", width=20),
                                    value="attachments",
                                ),
                                dmc.TabsTab(
                                    get_icon("bx:smile", width=20), value="stickers"
                                ),
                            ],
                            justify="center",
                        ),
                    ],
                    orientation="horizontal",
                    inverted=True,
                    w="100%",
                    h="100%",
                    value="stickers",
                    variant="outline",
                )
            ),
        ],
    )

    text_input_bar = dmc.Group(
        [
            dbc.InputGroup(
                [
                    DeferScript(src="/assets/scroll.js"),
                    dbc.Input(
                        placeholder="Cообщение", id="messenger-input-message_text"
                    ),
                    attachment_bar,
                    dbc.Button(get_icon("mdi:send", width=20), id="messenger-btn-send"),
                ],
            ),
            dbc.Button(
                get_icon("mdi:arrow-down", width=20),
                id="downClick",
                class_name="downClick",
            ),
        ],
        style={"flex-wrap": "nowrap"},
    )

    msg_threedots_menu = dmc.HoverCard(
        position="bottom",
        withArrow=True,
        width=270,
        shadow="md",
        children=[
            dmc.HoverCardTarget(
                dbc.Button(
                    get_icon(
                        icon_name="mdi:dots-horizontal",
                        width=25,
                    ),
                    outline=True,
                    color="primary",
                    id="messenger-btn-chat_actions",
                    class_name="p-1",
                ),
            ),
            dmc.HoverCardDropdown(
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Отключить уведомления",
                            color="primary",
                            outline=True,
                            id="messenger-btn-toggle_notif",
                            disabled=True
                        ),
                        dbc.Button(
                            "Удалить чат",
                            color="danger",
                            outline=True,
                            id="messenger-btn-delete_chat",
                        ),
                        dbc.Button(
                            "Заблокировать",
                            color="danger",
                            outline=True,
                            id="messenger-btn-ban",
                            disabled=True
                        ),
                    ],
                    vertical=True,
                    class_name="w-100",
                ),
            ),
        ],
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
                                id="messenger-btn-open_contacts_drawer",
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
                                        id="messenger-img-chat_partner",
                                    ),
                                    html.H5(
                                        "MotherOfGod",
                                        className="m-0",
                                        id="messenger-text-chat_partner_nickname",
                                    ),
                                ]
                            ),
                            span="auto",
                            className="ms-2",
                        ),
                        dmc.GridCol(
                            [
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
                            id="messenger-table-messages",
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
        className="boxx",
        gap=0,
    )

    return dmc.Stack(
        [
            modals,
            dmc.Drawer(
                dmc.Stack(
                    [
                        contacts,
                    ],
                    className="w-100",
                    gap=0,
                ),
                title=html.H5("Список контактов"),
                id="messenger-messenger-drawer-contacts",
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
                        className="d-flex adaptive-hide",
                    ),
                    dmc.GridCol(
                        messages,
                        span=9,
                        style={
                            "margin-bottom": "auto !important",
                        },
                        h="90dvh",  # DO NOT CHANGE!!! Breaks phone width
                        className="adaptive-width mt-0 p-0 mb-auto",
                    ),
                ],
                w="100%",
                h="100%",
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
    Output("messenger-drawer-contacts", "opened"),
    Input("messenger-btn-open_contacts_drawer", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_contacts(n_clicks):
    return True

# modal callbacks
im_modals.messenger_modal_addcontact_callback()
im_modals.messenger_modal_deletechat_callback()