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
from dash_extensions import DeferScript, Purify
from pages.messenger import im_modals
from controllers.token_validation import token_verify_controller

register_page(
    __name__,
    path="/im",
    icon="fa-solid:home",
    name="Dash Messenger",
)


def get_icon(icon_name, width, style=None):
    return DashIconify(icon=icon_name, width=width, style=style)


contact_global_classes = "tr-hover border-bottom w-100 leftside-msg"
contact_global_classes_active = " selected-tr"


def get_leftside_contacts(
    nickname,
    msg_text,
    index,
    msg_time="00:00",
    active=False,
    user_icon="/assets/user_icon.png",
    from_drawer=False,
):
    global contact_global_classes
    global contact_global_classes_active

    active_background = contact_global_classes_active if active else ""
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
        className=contact_global_classes + active_background,
        style={"margin": "10px"},
        id={"type": f"contacts-tab{'-drawer' if from_drawer else ''}", "index": index},
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
        [im_modals.messenger_modal_addcontact(), im_modals.messenger_modal_deletechat()]
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
                            disabled=True,
                        ),
                        dbc.Button(
                            "Добавить контакт",
                            color="primary",
                            outline=True,
                            id="messenger-btn-add_contact",
                            disabled=True,
                        ),
                    ],
                    vertical=True,
                    class_name="w-100",
                ),
            ),
        ],
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
                    disabled=True,
                )
            ),
            dmc.HoverCardDropdown(
                dmc.Tabs(
                    [
                        dmc.TabsPanel(
                            dmc.Stack(
                                [
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
                        placeholder="Cообщение",
                        id="messenger-input-message_text",
                        disabled=True,
                    ),
                    attachment_bar,
                    dbc.Button(
                        get_icon("mdi:send", width=20),
                        id="messenger-btn-send",
                        disabled=True,
                    ),
                ],
            ),
            dbc.Button(
                get_icon("mdi:arrow-down", width=20),
                id="downClick",
                class_name="downClick",
            ),
        ],
        style={"flex-wrap": "nowrap"},
        className="p-2",
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
                            disabled=True,
                        ),
                        dbc.Button(
                            "Удалить чат",
                            color="danger",
                            outline=True,
                            id="messenger-btn-delete_chat",
                            disabled=True,
                        ),
                        dbc.Button(
                            "Заблокировать",
                            color="danger",
                            outline=True,
                            id="messenger-btn-ban",
                            disabled=True,
                        ),
                    ],
                    vertical=True,
                    class_name="w-100",
                ),
            ),
        ],
    )

    contacts_drawer = dbc.Table(
        [
            get_leftside_contacts(
                "MotherOfGod", "Иди кушать уже", active=True, index=0, from_drawer=True
            )
        ]
        + [
            get_leftside_contacts(
                f"SuperDuper_{i+1}",
                "Ну как там с деньгами?",
                index=i + 1,
                from_drawer=True,
            )
            for i in range(20)
        ]
    )

    contacts = dbc.Table(
        [get_leftside_contacts("MotherOfGod", "Иди кушать уже", active=True, index=0)]
        + [
            get_leftside_contacts(
                f"SuperDuper_{i+1}",
                "Ну как там с деньгами?",
                index=i + 1,
            )
            for i in range(20)
        ]
    )

    return dbc.Table(
        [
            modals,
            dmc.Drawer(
                dmc.Stack(
                    [
                        contacts_drawer,
                    ],
                    className="w-100",
                    gap=0,
                ),
                title=html.H5("Список контактов"),
                id="messenger-drawer-contacts",
                padding="md",
                zIndex=10,
                size="90%",
            ),
            html.Thead(
                html.Tr(
                    [
                        html.Th(
                            dmc.Group(
                                [
                                    dbc.Input(
                                        placeholder="Поиск",
                                        style={"width": "12vw"},
                                        disabled=True,
                                    ),
                                    chats_threedots_menu,
                                ],
                                style={"width": "16vw"},
                                className="m-auto ps-2 adaptive-width-col",
                            ),
                            className="adaptive-hide border-start border-top",
                            style={"text-align": "center", "vertical-align": "middle"},
                        ),
                        html.Th(
                            [
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
                                        dmc.GridCol("MotherOfGod", span="auto"),
                                        dmc.GridCol(msg_threedots_menu, span="content"),
                                    ]
                                )
                            ],
                            style={"width": "100%"},
                            className="text-center border border-bottom-0",
                        ),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(
                                html.Div(
                                    contacts,
                                    style={"height": "100%", "overflow-y": "auto"},
                                ),
                                className="adaptive-hide border-top border-start messenger-screen-size",
                            ),
                            html.Td(
                                html.Div(
                                    dmc.Table(
                                        [
                                            get_message_tr(
                                                "MotherOfGod", html.P("Иди кушать уже!")
                                            ),
                                            get_message_tr(
                                                "Вы", html.P("Да щас, иду уже!")
                                            ),
                                        ]
                                        * 15,
                                        className="w-100 pe-1 mb-0 cover",
                                        highlightOnHover=True,
                                        striped=False,
                                        id="messenger-table-messages",
                                    ),
                                    style={"height": "100%", "overflow-y": "auto"},
                                    className="scroll-area",
                                ),
                                className="border border-bottom-0 messenger-screen-size",
                            ),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td(
                                dbc.Button(
                                    "Показать непрочитанные",
                                    class_name="btn btn-link",
                                    outline=True,
                                    disabled=True,
                                ),
                                className="adaptive-hide border",
                                style={"vertical-align": "middle"},
                            ),
                            html.Td(text_input_bar, className="border border-start-0"),
                        ]
                    ),
                ]
            ),
        ],
        className="mt-2 mb-0 table-borderless messenger-full-screen-size",
    )


@callback(
    Output("messenger-drawer-contacts", "opened", allow_duplicate=True),
    Input("messenger-btn-open_contacts_drawer", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_contacts(n_clicks):
    return True


@callback(
    Output({"type": "contacts-tab", "index": ALL}, "n_clicks"),
    Output({"type": "contacts-tab-drawer", "index": ALL}, "n_clicks"),
    Output({"type": "contacts-tab", "index": ALL}, "className"),
    Output({"type": "contacts-tab-drawer", "index": ALL}, "className"),
    Output("messenger-drawer-contacts", "opened"),
    Input({"type": "contacts-tab", "index": ALL}, "n_clicks"),
    Input({"type": "contacts-tab-drawer", "index": ALL}, "n_clicks"),
    prevent_inital_call=True,
)
def click_handle(n_clicks, n_clicks_drawer):
    global contact_global_classes
    global contact_global_classes_active

    from_drawer = False
    # work with desktop contacts tab
    if n_clicks == [None] * len(n_clicks):
        return_n_clicks = [no_update] * len(n_clicks)
        return_n_clicks_classname = [no_update] * len(n_clicks)
    else:
        print(f"Clicked on item {n_clicks.index(1)}")
        return_n_clicks = [None] * len(n_clicks)
        return_n_clicks_classname = [
            (
                contact_global_classes + contact_global_classes_active
                if i == 1
                else contact_global_classes
            )
            for i in n_clicks
        ]

    # work with mobile drawer contacts tab
    if n_clicks_drawer == [None] * len(n_clicks_drawer):
        return_n_clicks_drawer = [no_update] * len(n_clicks_drawer)
        return_n_clicks_drawer_classname = [no_update] * len(n_clicks_drawer)
    else:
        print(f"drawer Clicked on item {n_clicks_drawer.index(1)}")
        return_n_clicks_drawer = [None] * len(n_clicks_drawer)
        return_n_clicks_drawer_classname = [
            (
                contact_global_classes + contact_global_classes_active
                if i == 1
                else contact_global_classes
            )
            for i in n_clicks_drawer
        ]
        from_drawer = True

    return (
        return_n_clicks,
        return_n_clicks_drawer,
        return_n_clicks_classname,
        return_n_clicks_drawer_classname,
        False if from_drawer else no_update
    )



# modal callbacks
im_modals.messenger_modal_addcontact_callback()
im_modals.messenger_modal_deletechat_callback()

# auth token verify
token_verify_controller("im", from_im=True)
