FROM python:3.10

RUN mkdir /fastapi_trader

WORKDIR /fastapi_trader

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

#WORKDIR src
#
#CMD uvicorn main:app --host 0.0.0.0 --reload
