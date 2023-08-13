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
