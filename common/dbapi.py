import arrow

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from mihawk.common.config import mihawk_config
from mihawk.common.config import falcon_portal_config
from mihawk.common.config import uic_config
from mihawk.common.config import alarms_config

from mihawk.models.falcon_portal import Template
from mihawk.models.falcon_portal import Action
from mihawk.models.falcon_portal import Expression

from mihawk.models.uic import Team
from mihawk.models.uic import RelTeamUser
from mihawk.models.uic import User

from mihawk.models.alarms import EventCases
from mihawk.models.alarms import Events


mihawk_engine = create_engine(mihawk_config['sql_alchemy_conn'],
                              pool_size=100, max_overflow=100)

falcon_portal_engine = create_engine(falcon_portal_config['sql_alchemy_conn'],
                                     pool_size=200, max_overflow=100)

uic_engine = create_engine(uic_config['sql_alchemy_conn'],
                           pool_size=200, max_overflow=100)

alarms_engine = create_engine(alarms_config['sql_alchemy_conn'],
                              pool_size=200, max_overflow=100)


def commit(log):
    session = Session(bind=mihawk_engine)
    try:
        session.add(log)
        session.commit()
    except Exception as e:
        pass
    finally:
        session.close()


def get_user_contact_by_tpl_id(tpl_id, exp_id=0):

    session = Session(bind=falcon_portal_engine)

    if exp_id == 0:
        # 非expression，从templates过来
        # 拿到uic
        # select action.uic from tpl left join action on tpl.action_id = action.id where tpl.id = 2
        uic = (session.query(Template)
                      .from_self(Action.uic)
                      .join(Action, Template.action_id == Action.id)
                      .filter(Template.id == tpl_id)
                      .all())
    else:
        uic = (session.query(Expression)
                      .from_self(Action.uic)
                      .join(Action, Expression.action_id == Action.id)
                      .filter(Expression.id == exp_id)
                      .all())

    session.close()
    uic = uic[0][0]

    # 拿到所有的uid
    # select uid from team left join rel_team_user on
    #       team.id = rel_team_user.tid where team.name = '推荐系统RD'
    session = Session(bind=uic_engine)
    uids = (session.query(Team)
                   .from_self(RelTeamUser.uid)
                   .join(RelTeamUser, Team.id == RelTeamUser.tid)
                   .filter(Team.name == uic).all())
    uids = [item[0] for item in uids]

    # 拿到所有的邮箱，手机号以及微信号
    # select email, phone from user where id in (1, 2, 3);
    results = (session.query(User.name, User.email, User.phone, User.im)
                      .filter(User.id.in_(uids))
                      .all())
    session.close()
    return results


def get_infos_by_endpoint_metric_time(endpoint, metric, interval=10):

    session = Session(bind=alarms_engine)

    events = (session.query(EventCases)
                     .filter(EventCases.endpoint == endpoint)
                     .filter(EventCases.metric == metric)
                     .filter(EventCases.status == 'PROBLEM')
                     .all())

    res = list()
    for event in events:

        now = arrow.now().format('YYYY-MM-DD HH:mm:ss')
        ten_minutes_ago = arrow.now().replace(minutes=-interval).format('YYYY-MM-DD HH:mm:ss')

        count = len(session.query(Events)
                           .filter(Events.event_caseId == event.id)
                           .filter(Events.status == 0)
                           .filter(Events.timestamp >= ten_minutes_ago)
                           .filter(Events.timestamp <= now)
                           .all())
        res.append({
            "host": event.endpoint,
            "service": event.metric,
            "item": event.cond,
            "state": event.note,
            "count": count
        })
    session.close()

    return res
