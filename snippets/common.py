from configparser import ConfigParser


# 基础配置
base_config = ConfigParser()
base_config.read('/home/chengtao/mihawk/config.ini')

# mysql 配置
mysql_config = base_config['mysql']

# elasticsearch配置
elastic_config = base_config['elastic']

# 邮箱配置
mail_config = base_config['mail']
