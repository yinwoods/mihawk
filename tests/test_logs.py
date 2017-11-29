import json
import arrow

from mihawk.models.logs import Logs
from mihawk.snippets.dbapi import session


if __name__ == '__main__':

    logs = Logs(log_index='changba_user_action',
                time=arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                params='{"key": "value"}',
                response='{"key": "value"}')
    session.add(logs)
    session.commit()
    logs = session.query(Logs).filter(
            Logs.log_index == 'changba_user_action')
    for log in logs:
        print(log.log_index)
        print(log.time)
        params = json.loads(log.params)
        print(params)
        response = json.loads(log.response)
        print(response)
    session.close()
