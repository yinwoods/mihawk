# 常用的数据库封装函数
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from mihawk.snippets.common import mysql_config


engine = create_engine(mysql_config['sql_alchemy_conn'], echo=True)


def commit(log):
    session = Session(bind=engine)
    session.add(log)
    session.commit()
    session.close()


def latest_record(log_index, table):
    session = Session(bind=engine)
    assert 'time' in table.__dict__
    assert 'log_index' in table.__dict__
    return session.query(table).order_by(table.time.desc())\
                  .filter(table.log_index == log_index).first().response
