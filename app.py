from apistar import http
from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.backends import sqlalchemy_backend

from sqlalchemy.ext.declarative import declarative_base

from mihawk.snippets.alert import send_mail
from mihawk.snippets.common import mihawk_config


Base = declarative_base()


def alert(params: http.QueryParams):
    title = f'{params.get("endpoint", None)} {params.get("metric", None)}报警'
    message = dict(params)
    mail_result = send_mail(title, message, 'yinchengtao@4paradigm.com')
    response = {
        'mail': mail_result,
        'sms': 'NotImplemented',
    }
    return response


settings = {
    "DATABASE": {
        "URL": mihawk_config['sql_alchemy_conn'],
        "METADATA": Base.metadata
    }
}


routes_table = [
    Route('/alert', 'GET', alert),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(
    routes=routes_table,
    settings=settings,
    commands=sqlalchemy_backend.commands,
    components=sqlalchemy_backend.components
)


if __name__ == '__main__':
    app.main()
