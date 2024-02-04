FROM python:3.11
ENV PYTHONUNBUFFERED 1

# to create or restore a psql dump
RUN apt-get update
RUN apt-get install postgresql-client --yes
RUN apt-get install postgresql-client-common --yes
RUN apt-get install libpq-dev

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

# Move pipfiles to project.
ADD Pipfile Pipfile.lock ./

RUN pip install -U pip pipenv

RUN pipenv install --system --deploy
# copy migrations script
COPY ./scripts/migrations.sh /bin/migrations.sh
RUN chmod +x /bin/migrations.sh

RUN mkdir /src
COPY . /src/
WORKDIR /src

# Run collectstatic for whitenoise
#RUN python ./manage.py collectstatic --noinput

# Create empty env-file to avoid warnings
RUN touch ./.env

# Set variable for celery
ENV COLUMNS=80

EXPOSE 8000

CMD ["./scripts/run_backend.sh"]
