docker run -p 3306:3306 --restart on-failure:10 --name mihawk-mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:latest
