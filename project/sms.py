from apistar import http

from mihawk.common import dbapi
from mihawk.project.views import notify_sms


def notify(params: http.RequestData):

    content = params["content"]
    content = parse_content(content)

    if content.get("状态", "") == "OK":
        return {"sms": "misstatement"}

    endpoint = content.get("机器").strip()
    metric = content.get("指标").strip()
    tags = content.get("标签").strip().replace(":", "=")
    metric = metric + "/" + tags

    if "errcode=404" in metric:
        return {"sms": "misstatement"}
    if tags == "api=__serv__,errcode=415" or tags == "api=/dangdang/api/config,errcode=415":
        return {"sms": "misstatement"}
    # 目前的400错误先过滤掉，等待世举查明原因
    if tags == "api=__serv__,errcode=400" or tags == "api=/dangdang/api/log,errcode=400":
        return {"sms": "misstatement"}
    # zhulong 7k7k暂时不报警
    if "zhulong" in tags or "7k7k" in tags:
        return {"sms": "misstatement"}

    res = {
        "sms": {
            "to": params["tos"],
            "subject": f"{content.get('机器')} {content.get('标记')} 报警",
            "host": content.get("机器"),
            "service": metric,
            "item": content.get("表达式"),
            "state": content.get("标记")
        }
    }

    # 10分钟内出现3次或3次以上才报警
    events = dbapi.get_infos_by_endpoint_metric_time(endpoint, metric, interval=100)
    if len(events) == 0:
        return {"sms": "misstatement"}

    event = events[0]
    response = dict()
    response["sms"] = notify_sms(res) if event["count"] > 3 else "misstatement"
    return response


def parse_content(content):
    res = dict()
    content = content[1:-1].split("][")

    res["报警级别"], res["状态"], res["机器"], _, error_detail, time = content
    res["标记"], res["规则"], res["指标"], res["标签"], res["表达式"] = error_detail.split(" ")
    res["当前报警次数"], res["时间"] = time.split(" ", 1)

    return res
