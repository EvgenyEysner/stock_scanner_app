FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1

# Move pipfiles to project.
ADD Pipfile Pipfile.lock ./

RUN pip install -U pip pipenv
# copy migrations script
COPY ./scripts/migrations.sh /bin/migrations.sh
RUN chmod +x /bin/migrations.sh

RUN pipenv install --system --deploy

RUN mkdir /src
COPY . /src/
WORKDIR /src

# Run collectstatic for whitenoise
RUN python ./manage.py collectstatic --noinput

# Create empty env-file to avoid warnings
RUN touch ./.env

# Set variable for celery
ENV COLUMNS=80

EXPOSE 8000

CMD ["./scripts/run_backend.sh"]
