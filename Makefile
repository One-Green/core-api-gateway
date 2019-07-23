
create-su: ##@dev
	pipenv run python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" || echo "Error while creating admin"

updb: ##@dev
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate
	make create-su



