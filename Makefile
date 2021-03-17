-include .env

start-celery-workers:
	pipenv run celery -A project worker -l info

start-mqtt:
	docker rm mqtt-dev --force || true
	docker run  --name mqtt-dev -d  -p 8883:1883  -e MOSQUITTO_USERNAME=admin -e MOSQUITTO_PASSWORD=admin docker.io/shanisma/paho-mqtt:1.6.2

start-redis:
	docker rm redis-dev --force || true
	docker run --name redis-dev -d -p 6379:6379 redis:6.0.10-alpine

start-postgres:
	docker rm postgres-dev --force || true
	docker run --name postgres-dev -d -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres  postgres

migrate-db:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	pipenv run python init.py

start-services: start-postgres start-mqtt start-redis migrate-db start-celery-workers

start-api-gateway:
	pipenv run python manage.py runserver

core-unittest: core/tests/test_base_controller.py core/tests/test_base_time_range_controller.py
	cd ${PWD}/core/tests ;\
	pipenv run python test_base_controller.py ;\
	pipenv run python test_base_time_range_controller.py

run-tests: core-unittest

build-reset-builder:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	docker buildx rm build
	docker buildx create --use --name build --node build --driver-opt network=host
	docker buildx inspect --bootstrap

build: export TAG=0.0.1
build-dev:
	docker build -t docker.io/shanisma/pk-k8s-dev:${TAG} .
	docker push docker.io/shanisma/pk-k8s-dev:${TAG}


build-latest: export TAG=docker.io/shanisma/k8s-one-green:latest
build-latest:
	docker build -t ${TAG} .
	docker push ${TAG}

build: export TAG=0.0.1
build:
	docker buildx build -t docker.io/shanisma/pk-k8s:${TAG} \
	--platform linux/amd64,linux/arm64 \
	--push .

build-custom-mosquitto: export TAG=docker.io/shanisma/eclipse-mosquitto:1.6.2
build-custom-mosquitto: dependencies/example-mosquitto-simple-auth-docker-master/Dockerfile
	docker build -t ${TAG} -f dependencies/example-mosquitto-simple-auth-docker-master/Dockerfile
	docker push ${TAG}
