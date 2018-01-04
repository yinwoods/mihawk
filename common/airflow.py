import airflow


# airflow dag基础参数
default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'email_on_failure': True
}
