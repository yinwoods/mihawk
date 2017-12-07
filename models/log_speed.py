from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, JSON


Base = declarative_base()


class LogSpeed(Base):
    __tablename__ = 'log_speed'
    log_index = Column(String(50), nullable=False, primary_key=True)
    time = Column(TIMESTAMP, nullable=False, primary_key=True)
    params = Column(JSON)
    response = Column(JSON)
