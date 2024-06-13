FROM python:3.9-slim

WORKDIR /code

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY . .

RUN python3 -m venv /code/venv  && \
    /code/venv/bin/pip install -r /code/requirements.txt && \
    /code/venv/bin/python3 /code/models/models_to_local.py

CMD ["/code/venv/bin/fastapi", "run", "./main.py", "--port", "4200"]