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


def get_leftside_msg(nickname, msg_text, time='00:00', active=False):
    active_background = ' selected-tr' if active else ''
    # active_background = ''
    return html.Tr(
        [
            html.Td(
                html.Img(
                    src="/assets/user_icon.png",
                    className='transp-back user-icon'
                )
            ),
            html.Td(
                html.Div(
                    [
                        html.Strong(nickname),
                        html.Br(),
                        html.P(msg_text),
                        html.P(time, className='leftside-message-time')
                    ],
                    className="leftside-msg-text transp-back",
                ),
                className="w-100",
            ),
        ],
        className="tr-hover border-bottom w-100 leftside-msg"+active_background,
        style={"margin": "10px"},
        id=nickname
    )


def layout():
    contacts = html.Div(
        dbc.Table(
            [get_leftside_msg('MotherOfGod', 'Иди кушать уже', active=True)] +
            [
                get_leftside_msg('SuperDuper123', 'Ну как там с деньгами?'),
                get_leftside_msg('Order721', 'Где мой заказ, чушпанчик?')
            ]
            * 12,
            className="w-100 pe-1",
            hover=True,
        ),
        style={"overflow-y": "auto", "height": "85vh"},
    )

    return dmc.Stack(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        contacts,
                        span=3,
                        style={"background-color": "unset"},
                        # mih="100%",
                        # mah="100%",
                        className="adaptive-width",  # temp
                    ),
                    dmc.Col(
                        span=9,
                        style={"background-color": "unset"},
                        # mih="100%",
                        # mah="100%",
                        className="border-start adaptive-hide",
                    ),
                ],
                w="100%",
                h="100%",
                className="border",
                m="auto",
            )
        ],
        miw="100%",
        h="100%",
        justify="center",
    )

@callback(
    Output('MotherOfGod', 'n_clicks'),
    Input('MotherOfGod', 'n_clicks'),
    prevent_inital_call=True
)
def click_handle(n_clicks):
    # print('Clicked on row')
    return 0