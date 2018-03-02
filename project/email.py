from apistar import http

from mihawk.project.views import notify_email


def notify(params: http.RequestData):

    subject, content = params["subject"], params["content"]
    content = parse_content(content)

    if content["报警级别"] == "OK":
        return {"email": "misstatement"}

    table = {"content": [["属性", "值"]]}
    subject = table["title"] = f"{content.get('机器')} {content.get('标记')} 报警"

    for key, value in content.items():
        table["content"].append([key, value])

    res = {
        "email": {
            "to": params["tos"],
            "subject": subject
        },
        "tables": [
            table
        ]
    }

    return {"email": notify_email(res)}


def parse_content(content):
    content = content[:-1].split("\r\n")

    maps = {
        "endpoint": "机器",
        "metric": "指标",
        "tags": "标签",
        "note": "标记",
        "timestamp": "时间",
        "max": "最大报警次数",
        "current": "当前报警次数"
    }

    res = dict()
    res["报警级别"], res["状态"] = content[:2]

    res["规则地址"] = f"<a href={content[-1]}>{content[-1]}</a>" \
        if content[-1].startswith("http") else ""

    res["规则地址"] = res["规则地址"].replace(
            "http://127.0.0.1:8086", "https://recsys-falcon.4paradigm.com")

    for item in content[2:-1]:
        key, value = item.split(":", 1)
        key = key.lower()
        key = maps[key] if key in maps else key
        res[key] = value.strip()

    if "Current" in res.get(maps["max"], ""):
        max_val, curr = res[maps["max"]].split(",")
        res[maps["max"]] = max_val
        key, value = curr.strip().split(":")
        res[maps[key.lower()]] = value

    return res
