# hillel_py_pro_serge_ht_13
Hillel Python Pro course. Home task 13 (Celery)
Hillel Python Pro course. Home task 14 (Celery beat, Beautiful Soup)

# start page
http://127.0.0.1:8000/sel/sendemail/

# run celery for this project:
celery -A core worker -l INFO

# run Celery beat for this project:
celery -A core worker -B -l INFO

# manual parser launching
http://127.0.0.1:8000/sel/grabquotes/


# manage RabbitMQ
# stop the local node
sudo systemctl stop rabbitmq-server
# start it back
sudo systemctl start rabbitmq-server
# check on service status as observed by service manager
sudo systemctl status rabbitmq-server

# manage Redis
redis-server
redis-cli
    shutdown

# <-- run in Docker -->
# Celery doc:
docker run -d -p 5672:5672 rabbitmq
docker run -d -p 6379:6379 redis

# Pavel:
docker run -d --name rabbit -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin -p 5672:5672 -p 15672:15672 rabbitmq:3-management
docker run --name redis -p 6379:6379 -d redis

# Me:
docker run --name rabbit -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
docker run --name redis -d -p 6379:6379 redis
docker container stop rabbit redis
docker container start rabbit redis

# Doc on docker hub:
docker run -d --hostname my-rabbit --name some-rabbit rabbitmq:3
docker run -d --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management

