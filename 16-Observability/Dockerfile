FROM python:3.10

RUN mkdir src

COPY requirements.txt src
COPY app src/app
COPY main.py src

WORKDIR src
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["gunicorn", "main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UnicornWorker", "--bind", "0.0.0.0:8000"]
CMD ["gunicorn", "main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]