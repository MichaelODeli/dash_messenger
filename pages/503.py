from dash import html, register_page
import dash_mantine_components as dmc


register_page(__name__, name='503 | Dash Messenger')

def layout():
    return dmc.Stack(
        [
            html.H4('Сервер недоступен'),
            html.Img(src='https://http.cat/503', style={'max-width': '95vw'}),
            html.A(
                "Попробовать еще раз",
                style={"width": "content"},
                href='/',
                className='btn btn-primary'
            ),
        ],
        align="center",
        # justify="center",
        h="100%",
        pt="10vh",
        className="child-autoheight",
    )