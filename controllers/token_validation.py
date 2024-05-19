from dash import (
    dcc,
    Input,
    Output,
    callback,
    State,
    Input,
    Output,
    no_update,
)
from flask import request as flask_request
import requests


def token_verify_controller(source_page, from_im=False):
    @callback(
        Output(f"hidden_div_for_redirect_callback_{source_page}", "children"),
        Input(f"load_interval_{source_page}", "n_intervals"),
        State("token-store", "data"),
        running=[
            (Output("loading-overlay", "visible"), True, False),
        ] if not from_im else None
    )
    def redirector(n_intervals, token):
        hostname = flask_request.headers.get("Host").split(":")[0]
        print("stored token", token)
        if token != None:
            response = requests.get(
                f"http://{hostname}:5000/api",
                headers={"Authorization": token, "Sec-Fetch-Mode": "token_validation"},
            )
            token_test_result = response.content.decode("utf-8")
            if token_test_result == "True":
                print(f"user redirected to im page from {source_page}")
                return dcc.Location(pathname="/im", id=f"someid_doesnt_matter_{source_page}") if not from_im else no_update
            else:
                pass
    
        print(f"invalid stored token from {source_page}")
        return no_update if not from_im else dcc.Location(pathname="/", id=f"someid_doesnt_matter_{source_page}")
        # else:
        #     return no_update