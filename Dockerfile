FROM python:3.7.4
COPY . /app
WORKDIR /app
RUN rm Pipfile.lock || echo "Pipfile.lock not found"
RUN rm -r static || echo "static folder not found"
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --skip-lock