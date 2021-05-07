FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY __main__.py dataParsing.py dataReceiving.py dbManagement.py ./

CMD [ "python3", "__main__.py" ]