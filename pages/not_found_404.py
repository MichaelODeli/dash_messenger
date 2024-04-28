from dash import html, register_page
import dash_mantine_components as dmc


register_page(__name__, name='404 | Dash Messenger')

def layout():
    return dmc.Stack(
        [
            html.H4('Страница не найдена.'),
            html.Img(src='https://http.cat/404', style={'max-width': '95vw'}),
            html.A(
                "Вернуться на главную",
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