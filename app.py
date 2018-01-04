from apistar.frameworks.wsgi import WSGIApp as App
from apistar.backends import sqlalchemy_backend

from mihawk.project.routes import routes
from mihawk.common.config import settings


app = App(
    routes=routes,
    settings=settings,
    commands=sqlalchemy_backend.commands,
    components=sqlalchemy_backend.components
)


if __name__ == '__main__':
    app.main()
