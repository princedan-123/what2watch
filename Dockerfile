FROM python:3.12-slim-bookworm
COPY . /what2watch
WORKDIR /what2watch
RUN pip install -r  requirements.txt
