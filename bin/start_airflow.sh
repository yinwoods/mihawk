export AIRFLOW_HOME="$HOME/mihawk/airflow"
screen -S airflow webserver
screen -S airflow worker
screen -S airflow flower
screen -S airflow scheduler
