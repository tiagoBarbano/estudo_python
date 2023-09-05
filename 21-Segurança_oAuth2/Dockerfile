FROM python:3.10.9-slim-buster
RUN mkdir src

COPY requirements.txt src

COPY app src/app
COPY main.py src
COPY openssl src/openssl

WORKDIR src
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]