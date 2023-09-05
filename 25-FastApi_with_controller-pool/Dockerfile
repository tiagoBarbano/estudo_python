# FROM python:3.10.9-slim-buster

# RUN mkdir src

# COPY requirements.txt src
# COPY app src/app
# COPY main.py src

# WORKDIR src
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# EXPOSE 8000
# #CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]

# # Stage 1
# FROM python:3.10.9-slim-buster AS base

# RUN mkdir src
# COPY requirements.txt src
# WORKDIR src
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# # Stage 2
# FROM base AS final
# COPY app src/app
# COPY main.py src
# EXPOSE 8000
# CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]


# Stage 1 - compilação do código
FROM python:3.10.9-alpine as build

RUN mkdir src

COPY requirements.txt src
WORKDIR src
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev && \
        pip install --no-cache-dir --upgrade -r requirements.txt

# Stage 2 - criação da imagem final
FROM python:3.10.9-alpine
WORKDIR /app
COPY app src/app
COPY main.py src
EXPOSE 8000
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]