FROM python:3.7.4
COPY . /app
WORKDIR /app
RUN rm db.sqlite3 || echo "db.sqlite not found"
RUN rm Pipfile.lock || echo "Pipfile.lock not found"
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --skip-lock
RUN pipenv run python manage.py makemigrations --noinput
RUN pipenv run python manage.py makemigrations plant_core --noinput
RUN pipenv run python manage.py migrate
RUN pipenv run python manage.py collectstatic
RUN pipenv run python create_plant_keeper_user.py

CMD pipenv run gunicorn --workers=3 --bind 0.0.0.0:8001 --daemon plant_kiper.wsgi  &&\
    pipenv run python prometheus.py && \
    cd controllers && pipenv run python run.py

# Plant-keeper prometheus client
EXPOSE 8000/tcp
# Plant-keeper Rest API gateway
EXPOSE 8001/tcp