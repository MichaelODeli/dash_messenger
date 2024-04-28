"Главное окно мессенджера"
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
    path="/im",
    icon="fa-solid:home",
    name="Dash Messenger",
)


def layout():
    contacts = html.Div(
        [html.P('Контакт')]*50,
        className='scrollable-content',   
    )

    return dmc.Container(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        contacts,
                        span=3,
                        style={"background-color": "unset"},
                        # mih="100%",
                        # mah="100%",
                        className="adaptive-width",
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
                mah="100%",
                className="border",
            )
        ],
        miw="100%",
        # h="100%",
    )
