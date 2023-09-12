# Start a docker container based on the latest image.
docker run --name unir -itd          \
  -v /home/jeff/of/unir-tutelas:/mnt \
  ofiscal/tax.co:latest

docker exec -it unir bash

docker stop unir && docker rm unir
