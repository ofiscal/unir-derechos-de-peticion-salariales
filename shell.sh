# Start a docker container based on the latest image.
docker run --name unir -itd          \
  -v /home/jeff/of/unir-tutelas:/mnt \
  ofiscal/tax.co:latest

docker exec -it unir bash

docker stop unir && docker rm unir

# because `pytest` does not find local modules by default
PYTHONPATH=.:$PYTHONPATH pytest python/manipulate_files_test.py
