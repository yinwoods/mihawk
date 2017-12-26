from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls

from mihawk.project.views import alert

routes = [
    Route('/alert', 'GET', alert),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
