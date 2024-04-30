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
    style={"width": "100%"},
    className="border-bottom roww fit-content",
)

main_container = dmc.Grid(
    [
        dmc.GridCol(span=1, className="adaptive-hide"),
        # dmc.GridCol([dash.page_container], span=10, className='border border-top-0 adaptive-width', h='100%'),
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
    # className='adaptive-width',
    h="100%",
    p="0",
)


app.layout = dmc.MantineProvider(
    dmc.Container(
        [header, main_container],
        miw="100%",
        maw="100%",
        p="0",
        className="full-height boxx",
        # className='full-height'
    ),
    id="mantine_theme",
    defaultColorScheme="light",
)


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
