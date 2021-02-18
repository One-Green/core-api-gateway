-include .env

start-workers:
	pipenv run celery -A project worker -l info

api-gateway:
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
