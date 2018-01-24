from configparser import ConfigParser
from sqlalchemy.ext.declarative import declarative_base


# 基础配置
base_config = ConfigParser()
base_config.read('/home/chengtao/mihawk/config.ini')

# mihawk 配置
mihawk_config = base_config['mihawk']

# apistar 配置
Base = declarative_base()
settings = {
    "DATABASE": {
        "URL": mihawk_config['sql_alchemy_conn'],
        "METADATA": Base.metadata
    }
}

# falcon_portal 配置
falcon_portal_config = base_config['falcon_portal']

# uic 配置
uic_config = base_config['uic']

# elasticsearch配置
elastic_config = base_config['elastic']

# 邮箱配置
mail_config = base_config['mail']

# 短信配置
sms_config = base_config['sms']
