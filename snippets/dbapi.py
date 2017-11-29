from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from mihawk.snippets.common import mysql_config


engine = create_engine(mysql_config['sql_alchemy_conn'], echo=True)


def commit(logs):
    session = Session(bind=engine)
    session.add(logs)
    session.commit()
    session.close()
