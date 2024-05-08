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
import ast

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
            WebSocket(url="ws://127.0.0.1:5000/ws", id="ws"),
            dcc.Store(id="token-store", storage_type="local"),
            html.H3("Отладка методов WebSocket", className="text-center pb-2"),
            html.Div(id="ws-status"),
            dmc.Divider(),
            dmc.Group(
                [
                    html.H4("auth", className="mb-0"),
                    dbc.Input(
                        placeholder="username",
                        id="a-username",
                        style={"width": "200px"},
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
                        placeholder="email", id="rg-email", style={"width": "200px"}
                    ),
                    dbc.Input(
                        placeholder="password",
                        id="rg-password",
                        style={"width": "200px"},
                    ),
                    dbc.Button(
                        "Зарегаться",
                        id="rg",
                        style={"margin-left": "auto"},
                        disabled=True,
                    ),
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
                    dbc.Button(
                        "Выйти", id="lo", style={"margin-left": "auto"}, disabled=True
                    ),
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
                    dbc.Button(
                        "Чаты", id="gc", style={"margin-left": "auto"}, disabled=True
                    ),
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
                        "Сообщения в чате",
                        id="gm",
                        style={"margin-left": "auto"},
                        disabled=True,
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
                        style={"width": "200px"},
                    ),
                    dbc.Button(
                        "Отправить",
                        id="sm",
                        style={"margin-left": "auto"},
                        disabled=True,
                    ),
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
                        placeholder="content",
                        id="sgm-content",
                        style={"width": "200px"},
                    ),
                    dbc.Select(
                        id="sgm-contenttype",
                        options=[
                            {"label": "text", "value": "text"},
                            {"label": "picture", "value": "picture"},
                            {"label": "sticker", "value": "sticker"},
                        ],
                        value="text",
                        style={"width": "200px"},
                    ),
                    dbc.Button(
                        "Отправить в группу",
                        id="sgm",
                        style={"margin-left": "auto"},
                        disabled=True,
                    ),
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
    ),
)


# получение результатов и обновление соответствующих объектов
@app.callback(
    [
        Output("token-store", "data"),
        Output("ws-status", "children"),
        Output("a-resp", "children", allow_duplicate=True),
        Output("rg-resp", "children", allow_duplicate=True),
        Output("lo-resp", "children", allow_duplicate=True),
        Output("gc-resp", "children", allow_duplicate=True),
        Output("gm-resp", "children", allow_duplicate=True),
        Output("sm-resp", "children", allow_duplicate=True),
        Output("sgm-resp", "children", allow_duplicate=True),
    ],
    [Input("ws", "state"), Input("ws", "error"), Input("ws", "message")],
    State("token-store", "data"),
    prevent_initial_call=True,
)
def message(state, error, message, stored_token):
    token = stored_token
    if message != None:
        msg_data = ast.literal_eval(message["data"])
        if msg_data["mode"] == "auth":
            if msg_data["status"] == "200":
                token = msg_data["token"]
    else:
        msg_data = None

    return (
        [
            token,
            dmc.Stack(
                [
                    dcc.Markdown(f"**state**: {state}"),
                    dcc.Markdown(f"**error**: {error}"),
                    dcc.Markdown(f"**message**: {message}"),
                    dcc.Markdown(f"**token**: {token}"),
                ]
            ),
        ]
        + [str(msg_data) if msg_data != None else no_update]
        + [no_update] * 6
    )


# опрос форм и формирование итоговых запросов
@app.callback(
    Output("a-resp", "children"),
    Output("ws", "send", allow_duplicate=True),
    Input("a", "n_clicks"),
    State("a-username", "value"),
    State("a-password", "value"),
    prevent_initial_call=True,
)
def a(n_clicks, username, password):
    if None in [username, password]:
        return "No data provided", no_update
    else:
        message_structure = {
            "mode": "auth",
            "timestamp": None,
            "username": username,
            "password": password,
        }
        return no_update, str(message_structure)


@app.callback(
    Output("rg-resp", "children"),
    Output("ws", "send", allow_duplicate=True),
    Input("rg", "n_clicks"),
    State("rg-username", "value"),
    State("rg-email", "value"),
    State("rg-password", "value"),
    prevent_initial_call=True,
)
def rg(n_clicks, username, email, password):
    if None in [username, email, password]:
        return "No data provided", no_update
    return [no_update] * 2


@app.callback(
    Output("lo-resp", "children"),
    Output("ws", "send", allow_duplicate=True),
    Input("lo", "n_clicks"),
    State("lo-username", "value"),
    State("lo-token", "value"),
    prevent_initial_call=True,
)
def lo(n_clicks, username, token):
    if None in [username, token]:
        return "No data provided", no_update
    return [no_update] * 2


@app.callback(
    Output("gc-resp", "children"),
    Output("ws", "send", allow_duplicate=True),
    Input("gc", "n_clicks"),
    State("gc-token", "value"),
    prevent_initial_call=True,
)
def gc(n_clicks, token):
    if token == None:
        return "No data provided", no_update
    return [no_update] * 2


@app.callback(
    Output("gm-resp", "children"),
    Output("ws", "send", allow_duplicate=True),
    Input("gm", "n_clicks"),
    State("gm-token", "value"),
    State("gm-chatid", "value"),
    prevent_initial_call=True,
)
def gm(n_clicks, token, chat_id):
    if None in [chat_id, token]:
        return "No data provided", no_update
    return [no_update] * 2


@app.callback(
    Output("sm-resp", "children"),
    Output("ws", "send", allow_duplicate=True),
    Input("sm", "n_clicks"),
    State("sm-token", "value"),
    State("sm-chatid", "value"),
    State("sm-content", "value"),
    State("sm-contenttype", "value"),
    prevent_initial_call=True,
)
def sm(n_clicks, token, chat_id, content, content_type):
    if None in [chat_id, token, content, content_type]:
        return "No data provided", no_update
    return [no_update] * 2


@app.callback(
    Output("sgm-resp", "children"),
    Output("ws", "send"),
    Input("sgm", "n_clicks"),
    State("sgm-token", "value"),
    State("sgm-chatid", "value"),
    State("sgm-content", "value"),
    State("sgm-contenttype", "value"),
    prevent_initial_call=True,
)
def sgm(n_clicks, token, chat_id, content, content_type):
    if None in [chat_id, token, content, content_type]:
        return "No data provided", no_update
    return [no_update] * 2


server = app.server
app.config.suppress_callback_exceptions = True

dev = True

if __name__ == "__main__":
    if dev:
        app.run_server(debug=True, host="0.0.0.0", port=82)
    else:
        from waitress import serve

        serve(app.server, host="0.0.0.0", port=82)
