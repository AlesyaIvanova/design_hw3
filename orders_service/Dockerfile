FROM python:3.10

WORKDIR /orders_service

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8002

ENTRYPOINT ["python3", "main.py"]