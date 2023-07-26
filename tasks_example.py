"""
1. Install Celery
https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps
pip install celery

2. Install and configure Rabbitmq
https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html#id7
sudo apt-get install rabbitmq-server
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_user_tags myuser mytag
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
sudo rabbitmqctl status
sudo rabbitmq-server
sudo rabbitmq-server -detached
sudo rabbitmqctl stop

3. Running the Celery worker server
https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#running-the-celery-worker-server
celery -A tasks_example worker --loglevel=INFO

4. Calling the task
from tasks import add
add.delay(4, 4)

5. Install Redis-server
6. pip install redis
7.
redis-server --daemonize yes
sudo redis-server /etc/redis/redis.conf
redis-cli
a = add.delay(4, 4)
a.ready()
a.result

"""

from celery import Celery

app = Celery(
    'tasks_example',
    broker='pyamqp://guest@localhost//',
    # broker='pyamqp://admin:admin@localhost:5672/rabbitmq_host',
    backend='redis://localhost',
)


@app.task
def add(x, y):
    return x + y
