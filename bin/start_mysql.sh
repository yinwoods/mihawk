docker rm -f $(docker ps -aq --filter="name=mihawk-mysql")
docker run -p 3307:3306 -h mihawk-mysql --restart=always --name mihawk-mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:latest
