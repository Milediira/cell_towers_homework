Необходимо перейти в директорию airflow и выполнить там команду

~~~
cd airflow
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
~~~

и потом дописать то, что будет в .env в airflow/docker-compose.yml

Пример:

~~~
  environment:
    ...
    AIRFLOW_UID: 0
    AIRFLOW_GID: 0
~~~

После выполнения действий выше запустите команду в корне Вашего проекта:

~~~
bash run_docker.sh
~~~


На сервере может возникать ошибка PermissionError: [Errno 13] Permission denied: '/opt/airflow/logs/scheduler/'. 
Исправить можно, зайдя в директорию airflow и выполив команду:

~~~
chmod -R 777 logs/
~~~
