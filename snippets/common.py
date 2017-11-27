from configparser import ConfigParser


# 基础配置
base_config = ConfigParser()
base_config.read('/home/chengtao/mihawk/config.ini')

# elasticsearch 配置
elastic_config = base_config['elasticsearch']

# 邮箱配置
mail_config = base_config['mail']
