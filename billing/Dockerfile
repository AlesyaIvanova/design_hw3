FROM python:3.10

WORKDIR /billing

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8001

ENTRYPOINT ["python3", "main.py"]