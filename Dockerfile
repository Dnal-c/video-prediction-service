FROM python:3.12 as builder

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv

COPY requirements.txt .

RUN python -m ensurepip --upgrade && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.12

WORKDIR /app

ENV PATH="/app/venv/bin:$PATH"

COPY . .
COPY --from=builder /app/venv /app/venv

ENTRYPOINT ["/bin/bash","-c","./startup.sh"]