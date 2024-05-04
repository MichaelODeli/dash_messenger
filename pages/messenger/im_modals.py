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


def messenger_modal_addcontact():
    """Модалка для добавления контакта"""
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Добавить контакт")),
            dbc.ModalBody(
                html.Div(
                    [
                        dbc.Label(
                            "Введите ник собеседника",
                            html_for="messenger-input-add_contact_nickname",
                        ),
                        dbc.Input(
                            type="text",
                            id="messenger-input-add_contact_nickname",
                            placeholder="Введите никнейм",
                        ),
                    ],
                    className="mb-3",
                )
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Добавить",
                    id="messenger-btn-confirm_add_contact",
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
        id="messenger-modal-add_contact",
        is_open=False,
    )


def messenger_modal_addcontact_callback():
    @callback(
        Output("messenger-modal-add_contact", "is_open"),
        [
            Input("messenger-btn-add_contact", "n_clicks"),
            Input("messenger-btn-confirm_add_contact", "n_clicks"),
        ],
        [State("messenger-modal-add_contact", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open


def messenger_modal_deletechat(contact_name='Test123'):
    """Модалка для подтверждения удаления контакта"""
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(
                    "Подтверждение действия"
                )
            ),
            dbc.ModalBody(f"Вы действительно хотите удалить диалог с {contact_name}?"),
            dbc.ModalFooter(
                [dbc.Button(
                    "Да",
                    id="messenger-btn-confirm_delete_chat-yes",
                    className="ms-auto btn-danger",
                    n_clicks=0,
                ),
                dbc.Button(
                    "Нет",
                    id="messenger-btn-confirm_delete_chat-no",
                    n_clicks=0,
                )],
            ),
        ],
        id="messenger-modal-delete_chat",
        is_open=False,
    )


def messenger_modal_deletechat_callback():
    @callback(
        Output("messenger-modal-delete_chat", "is_open"),
        [
            Input("messenger-btn-confirm_delete_chat-yes", "n_clicks"),
            Input("messenger-btn-confirm_delete_chat-no", "n_clicks"),
            Input('messenger-btn-delete_chat', 'n_clicks')
        ],
        [State("messenger-modal-delete_chat", "is_open")],
    )
    def toggle_modal(n1, n2, n3, is_open):
        if n1 or n2 or n3:
            return not is_open
        return is_open
