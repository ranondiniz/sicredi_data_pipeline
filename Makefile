
up:
	docker-compose up --build

notebook:
	docker exec -it spark-jupyter bash

clean:
	rm -rf datalake/*
