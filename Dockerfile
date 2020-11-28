FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /gigmarketplace
WORKDIR /gigmarketplace
COPY requirements.txt /gigmarketplace/
RUN pip install -r requirements.txt
