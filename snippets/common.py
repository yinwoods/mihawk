from configparser import ConfigParser


# 基础配置
base_config = ConfigParser()
base_config.read('/home/chengtao/mihawk/config.ini')

# mihawk 配置
mihawk_config = base_config['mihawk']

# falcon_portal 配置
falcon_portal_config = base_config['falcon_portal']

# uic 配置
uic_config = base_config['uic']

# elasticsearch配置
elastic_config = base_config['elastic']

# 邮箱配置
mail_config = base_config['mail']
