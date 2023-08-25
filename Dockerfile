FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH="${PYTHONPATH}:/app" \
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

WORKDIR /app

RUN apt-get update -qqy && apt-get -qqy install -y default-libmysqlclient-dev default-mysql-client vim nano gcc nmap curl wget \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN rm -rf /var/lib/apt/lists/* /var/cache/apt/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN groupadd -g 1000 app

RUN useradd -g app --uid 1000 app

RUN chown -R app:app /app

USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
