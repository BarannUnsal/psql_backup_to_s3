FROM python:slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

RUN apt update && apt install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . $APP_HOME

CMD [ "python", "backup.py" ]
