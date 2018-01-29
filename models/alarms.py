from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP


Base = declarative_base()


class EventCases(Base):
    __tablename__ = 'event_cases'
    id = Column(String(50), nullable=False, primary_key=True)
    endpoint = Column(String(100), nullable=False)
    metric = Column(String(200), nullable=False)
    func = Column(String(50), nullable=False)
    cond = Column(String(200), nullable=False)
    note = Column(String(500))
    max_step = Column(Integer)
    current_step = Column(Integer)
    priority = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, )
    timestamp = Column(TIMESTAMP, nullable=False)
    update_at = Column(TIMESTAMP)
    closed_at = Column(TIMESTAMP)
    closed_note = Column(String(250))
    user_modified = Column(Integer)
    tpl_creator = Column(String(64))
    expression_id = Column(Integer)
    strategy_id = Column(Integer)
    template_id = Column(Integer)
    process_note = Column(Integer)
    process_status = Column(String(20))


class EventNote(Base):
    __tablename__ = 'event_note'
    id = Column(Integer, nullable=False, default=None, primary_key=True)
    event_caseId = Column(String(50))
    note = Column(Integer)
    cate_id = Column(String(20))
    status = Column(Integer)
    timestamp = Column(TIMESTAMP, nullable=False)
    user_id = Column(Integer)


class Events(Base):
    __tablename__ = 'events'
    id = Column(Integer, nullable=False, default=None, primary_key=True)
    event_caseId = Column(String(50))
    step = Column(Integer, nullable=False)
    cond = Column(String(200), nullable=False)
    status = Column(Integer, default=0)
    timestamp = Column(TIMESTAMP, nullable=False)
