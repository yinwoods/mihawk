from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, Integer

Base = declarative_base()


class RelTeamUser(Base):
    __tablename__ = 'rel_team_user'
    id = Column(Integer, nullable=False, default=None, primary_key=True)
    tid = Column(Integer, nullable=False, default=None)
    uid = Column(Integer, nullable=False, default=None)


class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, nullable=False, default=None, primary_key=True)
    name = Column(String(64), nullable=False)
    resume = Column(String(255), nullable=False)
    creator = Column(String(64), nullable=False)
    created = Column(TIMESTAMP, nullable=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, default=None, primary_key=True)
    name = Column(String(64), nullable=False)
    passwd = Column(String(64), nullable=False)
    cnname = Column(String(128), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(16), nullable=False)
    im = Column(String(32), nullable=False)
    qq = Column(String(16), nullable=False)
    role = Column(Integer, nullable=False, default=0)
    creator = Column(Integer, nullable=False, )
    created = Column(TIMESTAMP, nullable=False)
