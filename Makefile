build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

stop-broker1:
	docker-compose stop kafka1

stop-broker2:
	docker-compose stop kafka2

stop-consumer:
	docker-compose stop consumer

start-broker1:
	docker-compose start kafka1

start-broker2:
	docker-compose start kafka2

start-consumer:
	docker-compose start consumer
