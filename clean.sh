#!/bin/bash

docker-compose down
docker rmi geo-query-engine
docker rmi mongo:4.2

# remove exited containers
docker container prune -f
# remove all images tagged with <none>
docker rmi $(docker images -f "dangling=true" -q)

echo "Done cleaning up the geo-query-engine container."
