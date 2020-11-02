import os

host = os.environ.get('APP_HOST', '0.0.0.0')
port = os.environ.get('APP_PORT', 8000)
workers = os.environ.get('APP_WORKERS', 1)
threads = os.environ.get('APP_THREADS', 1)
request = os.environ.get('APP_REQUEST', 1)
max_requests = os.environ.get('APP_MAX_REQUESTS', 0)
max_requests_jitter = os.environ.get('APP_MAX_REQUESTS_JITTER', 0)
flavour = os.environ.get('APP_FLAVOUR', '')


bind = f'{host}:{port}'
loglevel = os.environ.get('APP_GUNICORN_LOGLEVEL', 'debug')
capture_output = True
