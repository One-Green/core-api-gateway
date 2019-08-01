-include .env

updb: ##@dev
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate

create-su: ##@dev
	-pipenv run python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" || echo "Error while creating admin"

runserver:
	pipenv run python manage.py runserver

dj-shell:
	pipenv run python manage.py shell -i ipython


core-unittest: core/tests/test_base_controller.py core/tests/test_base_time_range_controller.py
	cd ${PWD}/core/tests ;\
	pipenv run python test_base_controller.py ;\
	pipenv run python test_base_time_range_controller.py

run-tests: core-unittest