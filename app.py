#
# Import libs
#
import dash
from dash import (
    html,
    Output,
    Input,
    State,
    callback,
    dcc,
    clientside_callback,
    no_update,
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_extensions import WebSocket
from flask import request as flask_request

#
# app config
#
dash._dash_renderer._set_react_version("18.2.0")
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME],
    title="Dash Messenger",
    update_title="Dash Messenger 🔄️",
    external_scripts=[
        "/assets/size.js",
        "https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js",
    ],
)

temp_buttons = dmc.Group(
    [
        html.A(
            "Мессенджер",
            style={"width": "content"},
            className="btn btn-primary btn-sm",
            href="/im",
        ),
        html.A(
            "Управление аккаунтом",
            style={"width": "content"},
            className="btn btn-primary btn-sm",
            href="/account/manage",
        ),
        dbc.Button("Выход", size="sm", id="header-btn-logout"),
    ],
    pr="10px",
)

#
# static layout
#
header = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Dash Messenger", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Row(
                    [
                        dbc.Col(temp_buttons),
                        dbc.Col(
                            html.Span(
                                [
                                    dbc.Label(
                                        className="fa fa-moon",
                                        html_for="color-mode-switch",
                                        color="secondary",
                                    ),
                                    dbc.Switch(
                                        id="color-mode-switch",
                                        value=True,
                                        className="d-inline-block ms-1",
                                        persistence=True,
                                    ),
                                    dbc.Label(
                                        className="fa fa-sun",
                                        html_for="color-mode-switch",
                                        color="secondary",
                                    ),
                                ]
                            ),
                            width="auto",
                        ),
                    ],
                    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                    align="center",
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    style={"width": "100%", 'position': 'absolute'},
    className="border-bottom roww fit-content",
)

main_container = dmc.Grid(
    [
        dcc.Store(id="token-store", storage_type="local"),
        WebSocket(url=f"ws://192.168.3.36:5000/ws", id="ws"),
        dcc.Interval(
            id="load_interval",
            n_intervals=0,
            max_intervals=0,  # <-- only run once
            interval=1,
        ),
        html.Div(id="hidden_div_for_redirect_callback"),
        html.Div(id="hidden_div_for_redirect_callback_logout"),

        dmc.GridCol(span=1, className="adaptive-hide"),
        dmc.GridCol(
            dash.page_container,
            span=10,
            className="adaptive-width child-height-100",
            h="100%",
        ),
        dmc.GridCol(span=1, className="adaptive-hide"),
    ],
    align="center",
    className="roww fill-remain",
    h="100%",
    pt="3rem",
)


app.layout = dmc.MantineProvider(
    dmc.Container(
        [header, main_container],
        miw="100%",
        maw="100%",
        p="0",
        className="full-height boxx",
    ),
    id="mantine_theme",
    defaultColorScheme="light",
)


# update websocket server ip
@app.callback([Output("ws", "url"), Input("load_interval", "n_intervals")])
def url_update(n_intervals):
    hostname = flask_request.headers.get("Host").split(":")[0]
    return [f"ws://{hostname}:5000/ws"]


@app.callback(
    Output("hidden_div_for_redirect_callback", "children"),
    Input("ws", "state"),
    prevent_initial_call=True,
)
def ws_error_handle(ws_state):
    if ws_state == None:
        return no_update

    if ws_state["readyState"] == 3:
        return dcc.Location(pathname="/503", id="someid_doesnt_matter")
    else:
        return no_update


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output("mantine_theme", "forceColorScheme"), Input("color-mode-switch", "value")
)
def make_mantine_theme(value):
    return "dark" if value == False else "light"


@callback(
    Output("hidden_div_for_redirect_callback_logout", "children"),
    Output("token-store", "data", allow_duplicate=True),
    Output("ws", "send", allow_duplicate=True),
    Input("header-btn-logout", "n_clicks"),
    State("token-store", "data"),
    prevent_initial_call=True,
)
def preform_logout(n_clicks, token):
    print('logout trigger')
    if token != None:
        message_structure = str({
            "mode": "logout",
            "timestamp": "None",
            "token": token,
        })
    else:
        message_structure = no_update

    return (
        dcc.Location(pathname="/", id="someid_doesnt_matter_logout"),
        None,
        message_structure,
    )


clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

#
# Dash server launcher
#
server = app.server
app.config.suppress_callback_exceptions = True

dev = True

if __name__ == "__main__":
    if dev:
        app.run_server(debug=True, host="0.0.0.0", port=82)
    else:
        from waitress import serve

        serve(app.server, host="0.0.0.0", port=82)
