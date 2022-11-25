FROM python:3.10
RUN mkdir src

COPY requirements.txt src

COPY app src/app
COPY main.py src

WORKDIR src
RUN pip install --no-cache-dir --upgrade certifi
RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]