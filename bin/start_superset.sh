docker rm -f $(docker ps -aq --filter="name=mihawk-superset")
docker run -p 8088:8088 -h mihawk-superset --link mihawk-mysql:mysql --restart=always -v $PWD/../superset/:/etc/superset  --name mihawk-superset -d amancevice/superset
