from apistar.frameworks.wsgi import WSGIApp as App
from apistar.backends import sqlalchemy_backend

from sqlalchemy.ext.declarative import declarative_base

from mihawk.snippets.common import mihawk_config
from mihawk.project.routes import routes


Base = declarative_base()


settings = {
    "DATABASE": {
        "URL": mihawk_config['sql_alchemy_conn'],
        "METADATA": Base.metadata
    }
}


app = App(
    routes=routes,
    settings=settings,
    commands=sqlalchemy_backend.commands,
    components=sqlalchemy_backend.components
)


if __name__ == '__main__':
    app.main()
