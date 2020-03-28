-include .env

up-raspap:
	# install RaspAP to create Wifi acces point for Node-Devices
	wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap

up-django: ##@dev
	rm -rv plant_core/migrations || true
	pipenv run python manage.py makemigrations plant_core
	pipenv run python manage.py migrate
	pipenv run python manage.py collectstatic

up-grafana:
	# download and install Granafa
	wget https://dl.grafana.com/oss/release/grafana_6.3.3_armhf.deb
	sudo dpkg -i grafana_6.3.3_armhf.deb
	# ethernet to localport 3000>3000
	sudo iptables -t nat -A PREROUTING -p tcp --dport 3000 -j REDIRECT --to-port 3000


create-su: ##@dev
	-pipenv run python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" || echo "Error while creating admin"

runserver-dev:
	pipenv run python manage.py runserver

dj-shell:
	pipenv run python manage.py shell -i ipython


core-unittest: core/tests/test_base_controller.py core/tests/test_base_time_range_controller.py
	cd ${PWD}/core/tests ;\
	pipenv run python test_base_controller.py ;\
	pipenv run python test_base_time_range_controller.py

run-tests: core-unittest

buildx: export TAG=0.0.1
buildx:
	docker buildx build \
	--platform linux/arm64 \
	--tag shanisma/plant-keeper:${TAG} \
	--push .

build-push-base: export TAG=0.0.1
build-push-base:
	docker login
	docker build -t shanisma/plant-keeper:${TAG} -f Dockerfile.base .
	docker push shanisma/plant-keeper:${TAG}
