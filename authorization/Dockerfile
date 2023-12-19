FROM python:3.10

WORKDIR /authorization

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8008

ENTRYPOINT ["python3", "main.py"]