from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.backends import sqlalchemy_backend

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from mihawk.snippets.common import mysql_config


Base = declarative_base()


class Rule(Base):
    __tablename__ = 'Rule'
    id = Column(Integer, primary_key=True)
    type = Column(String)


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to ApiStar!'}
    return {'message': f'Welcome to Apistar!, {name}'}


def append_rule():
    # 添加一个新的监控规则
    return {}


def delete_rule(rule_id: str):
    # 删除一个监控规则
    return {}


def query_rule(rule_id: str):
    # 查询监控规则
    return {}


def change_rule(rule_id: str):
    # 修改监控规则
    return {}


settings = {
    "DATABASE": {
        "URL": mysql_config['sql_alchemy_conn'],
        "METADATA": Base.metadata
    }
}


routes_table = [
    Route('/', 'GET', welcome),
    Route('/', 'POST', append_rule),
    Route('/{rule_id}', 'DELETE', delete_rule),
    Route('/{rule_id}', 'GET', query_rule),
    Route('/{rule_id}', 'PUT', change_rule),
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
