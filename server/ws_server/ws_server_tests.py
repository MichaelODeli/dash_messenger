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

dash._dash_renderer._set_react_version("18.2.0")
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME],
    title="Dash WebSocket Tests",
    update_title="Dash WebSocket Tests 🔄️",
    external_scripts=[
        "/assets/size.js",
        "https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js",
    ],
)

app.layout = dmc.MantineProvider(
    dmc.Stack(
        [
            html.H3('Отладка методов WebSocket', className='text-center pb-2'),
            dmc.Group(
                [
                    html.H4("auth", className="mb-0"),
                    dbc.Input(
                        placeholder="login", id="a-login", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="password",
                        id="a-password",
                        style={"width": "200px"},
                    ),
                    dbc.Button("Войти", id="a", style={"margin-left": "auto"}),
                ],
                w="100%",
                align="center",
            ),
            html.Div(id="a-resp"),
            dmc.Divider(),
            dmc.Group(
                [
                    html.H4("register", className="mb-0"),
                    dbc.Input(
                        placeholder="username",
                        id="rg-username",
                        style={"width": "200px"},
                    ),
                    dbc.Input(
                        placeholder="login", id="rg-login", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="password",
                        id="rg-password",
                        style={"width": "200px"},
                    ),
                    dbc.Button("Зарегаться", id="rg", style={"margin-left": "auto"}),
                ],
                w="100%",
                align="center",
            ),
            html.Div(id="rg-resp"),
            dmc.Divider(),
            dmc.Group(
                [
                    html.H4("logout", className="mb-0"),
                    dbc.Input(
                        placeholder="token", id="lo-token", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="username",
                        id="lo-username",
                        style={"width": "200px"},
                    ),
                    dbc.Button("Выйти", id="lo", style={"margin-left": "auto"}),
                ],
                w="100%",
                align="center",
            ),
            html.Div(id="lo-resp"),
            dmc.Divider(),
            dmc.Group(
                [
                    html.H4("getChats", className="mb-0"),
                    dbc.Input(
                        placeholder="token", id="gc-token", style={"width": "200px"}
                    ),
                    dbc.Button("Чаты", id="gc", style={"margin-left": "auto"}),
                ],
                w="100%",
                align="center",
            ),
            html.Div(id="gc-resp"),
            dmc.Divider(),
            dmc.Group(
                [
                    html.H4("getMessages", className="mb-0"),
                    dbc.Input(
                        placeholder="token", id="gm-token", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="chat_id", id="gm-chatid", style={"width": "200px"}
                    ),
                    dbc.Button(
                        "Сообщения в чате", id="gm", style={"margin-left": "auto"}
                    ),
                ],
                w="100%",
                align="center",
            ),
            html.Div(id="gm-resp"),
            dmc.Divider(),
            dmc.Group(
                [
                    html.H4("sendMessage", className="mb-0"),
                    dbc.Input(
                        placeholder="token", id="sm-token", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="chat_id", id="sm-chatid", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="content", id="sm-content", style={"width": "200px"}
                    ),
                    dbc.Select(
                        id="sm-contenttype",
                        options=[
                            {"label": "text", "value": "text"},
                            {"label": "picture", "value": "picture"},
                            {"label": "sticker", "value": "sticker"},
                        ],
                        value="text",
                        style={"width": "200px"}
                    ),
                    dbc.Button("Отправить", id="sm", style={"margin-left": "auto"}),
                ],
                w="100%",
                align="center",
            ),
            html.Div(id="sm-resp"),
            dmc.Divider(),
            dmc.Group(
                [
                    html.H4("sendGroupMessage", className="mb-0"),
                    dbc.Input(
                        placeholder="token", id="sgm-token", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="chat_id", id="sgm-chatid", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="content", id="sgm-content", style={"width": "200px"}
                    ),
                    dbc.Select(
                        id="sgm-contenttype",
                        options=[
                            {"label": "text", "value": "text"},
                            {"label": "picture", "value": "picture"},
                            {"label": "sticker", "value": "sticker"},
                        ],
                        value="text",
                        style={"width": "200px"}
                    ),
                    dbc.Button("Отправить в группу", id="sgm", style={"margin-left": "auto"}),
                ],
                w="100%",
                align="center",
            ),
            html.Div(id="sgm-resp"),
            dmc.Divider(),

        ],
        ps="15vw",
        pe="15vw",
        pt="5vh",
    )
)


server = app.server
app.config.suppress_callback_exceptions = True

dev = True

if __name__ == "__main__":
    if dev:
        app.run_server(debug=True, host="0.0.0.0", port=82)
    else:
        from waitress import serve

        serve(app.server, host="0.0.0.0", port=82)
