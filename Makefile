-include .env

core-unittest: core/tests/test_base_controller.py core/tests/test_base_time_range_controller.py
	cd ${PWD}/core/tests ;\
	pipenv run python test_base_controller.py ;\
	pipenv run python test_base_time_range_controller.py

run-tests: core-unittest

build-reset-builder:
	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	docker buildx rm builder
	docker buildx create --name builder --driver docker-container --use
	docker buildx inspect --bootstrap

build: export TAG=0.0.1
build:
	docker buildx build -t docker.io/shanisma/pk-k8s:${TAG} \
	--platform linux/amd64,linux/arm64,linux/armhf \
	--push .
