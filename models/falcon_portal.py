from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP


Base = declarative_base()


class Action(Base):
    __tablename__ = 'action'
    id = Column(Integer, nullable=False, default=None, primary_key=True)
    uic = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    callback = Column(Integer, nullable=False, default=0)
    before_callback_sms = Column(Integer, nullable=False, default=0)
    before_callback_mail = Column(Integer, nullable=False, default=0)
    after_callback_sms = Column(Integer, nullable=False, default=0)
    after_callback_mail = Column(Integer, nullable=False, default=0)


class Template(Base):
    __tablename__ = 'tpl'
    id = Column(Integer, nullable=False, default=None, primary_key=True)
    tpl_name = Column(String(255), nullable=False)
    parent_id = Column(Integer, nullable=False, default=0)
    action_id = Column(Integer, nullable=False, default=0)
    create_user = Column(String(64), nullable=False, )
    create_at = Column(TIMESTAMP, nullable=False)
