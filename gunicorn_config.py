# gunicorn_config.py
workers = 9  # Adjust based on your CPU cores
threads = 4  # Number of threads per worker
bind = '0.0.0.0:8501'
