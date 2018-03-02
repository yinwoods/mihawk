from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls

from mihawk.project import email
from mihawk.project import sms
from mihawk.project import wechat

from mihawk.project.views import alert
from mihawk.project.views import notify_email
from mihawk.project.views import notify_sms

routes = [
    Route("/email", "POST", name="email", view=email.notify),
    Route("/sms", "POST", name="sms", view=sms.notify),
    Route("/wechat", "POST", name="wechat", view=wechat.notify),
    Route("/alert", "GET", alert),
    Route("/notify/email", "POST", notify_email),
    Route("/notify/sms", "POST", notify_sms),
    Include("/docs", docs_urls),
    Include("/static", static_urls)
]
