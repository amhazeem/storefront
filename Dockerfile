FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /storefront
WORKDIR /storefront
COPY requirements.txt /storefront/
RUN pip install -r requirements.txt
