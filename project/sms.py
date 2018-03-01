import json
from apistar import http

from mihawk.common import dbapi
from mihawk.common.alert import send_mail
from mihawk.project.views import notify_sms


def notify(params: http.RequestData):

    content = params["content"]
    content = parse_content(content)

    maps = ["机器", "指标", "标签", "标记", "时间", "最大报警次数", "当前报警次数"]

    res = {
        "sms": {
            "to": params["tos"],
            "subject": f"{content.get('机器')} {content.get('标记')} 报警",
            "host": content.get("机器"),
            "service": json.dumps(dict(zip(maps, [content.get(key) for key in maps]))),
            "item": f"{content.get('机器')} {content.get('标记')} 报警",
            "state": content.get("表达式")
        }
    }

    endpoint = content.get("机器").strip()
    metric = content.get("指标").strip()
    tags = content.get("标签").strip().replace(":", "=")
    metric = metric + "/" + tags

    # 10分钟内出现3次或3次以上才报警
    events = dbapi.get_infos_by_endpoint_metric_time(endpoint, metric, interval=10)
    if len(events) == 0:
        return {"sms": "misstatement"}

    event = events[0]
    response = dict()
    response["sms"] = notify_sms(res) if event["count"] > 3 else "misstatement"
    return response


def parse_content(content):
    res = dict()
    content = content[1:-1].split("][")

    res["状态"], res["报警级别"], res["机器"], _, error_detail, time = content
    res["标记"], res["规则"], res["指标"], res["标签"], res["表达式"] = error_detail.split(" ")
    res["当前报警次数"], res["时间"] = time.split(" ", 1)

    return res
