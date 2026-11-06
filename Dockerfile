FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Unprivileged runtime user; /data holds the SQLite DB (mounted volume).
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /data && chown app /data
USER app

EXPOSE 8000
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", \
     "--worker-tmp-dir", "/tmp", "--no-control-socket", \
     "--access-logfile", "-", "run:app"]
