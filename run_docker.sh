echo killing old docker processes
docker-compose -f airflow/docker-compose.yml rm -fs
docker-compose -f clickhouse_collect_data/docker-compose.yml rm -fs

echo building docker containers
docker-compose -f airflow/docker-compose.yml up -d --build
docker-compose -f clickhouse_collect_data/docker-compose.yml up -d --build


