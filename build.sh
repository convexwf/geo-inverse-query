#!/bin/bash

docker-compose build --no-cache
docker-compose up -d

docker exec -it geo-query-engine /bin/bash -c "cd /app && bash ./get_ok_geo_csv.sh"
docker exec -it geo-query-engine /bin/bash -c "cd /app && python3 extract_ok_geo.py"
docker exec -it geo-query-engine /bin/bash -c "cd /app && python3 geo_engine.py --import_geo_data"

echo "Done building and running the geo-query-engine container."
echo "To enter the container, run: bash dev_into.sh or docker exec -it geo-query-engine /bin/bash"
