docker-compose down --remove-orphans
docker volume rm $(docker volume ls -q)
docker-compose up -d
