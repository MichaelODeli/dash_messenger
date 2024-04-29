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
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

register_page(
    __name__,
    path="/im",
    icon="fa-solid:home",
    name="Dash Messenger",
)


def get_leftside_msg(nickname, msg_text, time="00:00", active=False):
    active_background = " selected-tr" if active else ""
    return html.Tr(
        [
            html.Td(
                html.Img(src="/assets/user_icon.png", className="transp-back user-icon")
            ),
            html.Td(
                html.Div(
                    [
                        html.Strong(nickname),
                        html.Br(),
                        html.P(msg_text),
                        html.P(time, className="leftside-message-time"),
                    ],
                    className="leftside-msg-text transp-back",
                ),
                className="w-100",
            ),
        ],
        className="tr-hover border-bottom w-100 leftside-msg" + active_background,
        style={"margin": "10px"},
        id=nickname,
    )


def layout():
    contacts = dmc.ScrollArea(
        dbc.Table(
            [get_leftside_msg("MotherOfGod", "Иди кушать уже", active=True)]
            + [
                get_leftside_msg("SuperDuper123", "Ну как там с деньгами?"),
                get_leftside_msg("Order721", "Где мой заказ, челик?"),
            ]
            * 12,
            className="w-100 pe-1 mb-0",
            hover=True,
        ),
        mah="100%",
        type="auto",
        m="auto",
        w="100%",
        offsetScrollbars=True,
        className="dynamic-scroll-height",
    )

    text_input_bar = dbc.InputGroup(
        [
            dbc.Input(placeholder="Ваше сообщение", id="message-text"),
            dbc.Button(html.Div(className="fa fa-paperclip"), disabled=True),
            dbc.Button("Отправить", id="send-message"),
            dbc.Button(
                html.Div(className="fa fa-arrow-down"),
                disabled=True,
                id="scroll-to-bottom",
            ),
        ],
    )

    messages_scroll = dmc.ScrollArea(
        dbc.Table(
            [
                get_leftside_msg("SuperDuper123", "Ну как там с деньгами?"),
                get_leftside_msg("Order721", "Где мой заказ, челик?"),
            ]
            * 12,
            className="w-100 pe-1 mb-0",
            hover=True,
        ),
        type="auto",
        offsetScrollbars=True,
        className="h-100 w-100",
    )

    messages = dmc.Stack(
        [
            html.Div(
                dmc.Grid(
                    [
                        dmc.GridCol(
                            dbc.Button(
                                DashIconify(
                                    icon="material-symbols:menu-rounded",
                                    width=25,
                                ),
                                outline=True,
                                color="primary",
                                style={"padding": "var(--bs-btn-padding-y)"},
                                id="open-contacts-drawer",
                            ),
                            span="content",
                            className="adaptive-show",
                        ),
                        dmc.GridCol(
                            html.Center("SuperDuper123", className="h5 m-0"),
                            span="auto",
                        ),
                        dmc.GridCol(
                            dbc.Button(
                                DashIconify(
                                    icon="mdi:dots-horizontal",
                                    width=25,
                                ),
                                outline=True,
                                color="primary",
                                style={"padding": "var(--bs-btn-padding-y)"},
                            ),
                            span="content",
                        ),
                    ],
                    gutter="xs",
                ),
                className="w-100 roww fit-content border-bottom",
            ),
            html.Div(
                messages_scroll,
                className="w-100 roww fill-remain",
            ),
            html.Div(
                text_input_bar,
                className="w-100 roww fit-content border-top",
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
                messages_scroll,
                title=html.H5("Список контактов"),
                id="drawer-contacts",
                padding="md",
                zIndex=10000,
                size="90%",
            ),
            dmc.Grid(
                [
                    dmc.GridCol(
                        contacts,
                        span=3,
                        style={"background-color": "unset"},
                        mih="100%",
                        p=0,
                        className="d-flex adaptive-hide",  # temp
                    ),
                    dmc.GridCol(
                        messages,
                        span=9,
                        style={
                            "background-color": "unset",
                            "margin-bottom": "auto !important",
                        },
                        h="90dvh",
                        className="border-start adaptive-width mt-0 p-0 mb-auto",
                    ),
                ],
                w="100%",
                h="100%",
                className="border",
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
