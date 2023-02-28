FROM python:3.10-slim-bullseye AS builder

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

FROM builder as runner

RUN pip3 install -U uvicorn --no-cache-dir
COPY ./docker_entrypoint /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
#CMD ["-m", "uvicorn", "--host", "", "--port", "8000", "dbms_theory_backend.asgi:application"]
