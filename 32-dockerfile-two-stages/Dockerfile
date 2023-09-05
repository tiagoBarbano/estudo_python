# Stage 1
FROM python:3.10-slim-buster AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Stage 2
FROM base AS final
COPY . .
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]