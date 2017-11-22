from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from project.routes import routes


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to ApiStar!'}
    return {'message': f'Welcome to Apistar!, {name}'}


routes = [
    Route('/', 'GET', welcome),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
