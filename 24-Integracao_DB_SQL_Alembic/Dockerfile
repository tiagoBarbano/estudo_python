FROM python:3.10
RUN mkdir src

COPY requirements.txt src

COPY app src/app
COPY main.py src
COPY startup.sh src
COPY .env src

WORKDIR src
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

# RUN chmod +x startup.sh

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD [ "chmod", "+x", "startup.sh"]