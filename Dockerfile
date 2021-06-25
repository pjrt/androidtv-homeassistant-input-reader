# FROM python:3.8
FROM alpine:3.14

USER root
WORKDIR /root

RUN apk add --update --no-cache python3 py-pip android-tools && \
    pip install pure-python-adb requests && \
    ln -sf python3 /usr/bin/python

ADD androidTVController.py .
ADD entrypoint.sh .

CMD ["sh", "/root/entrypoint.sh"] 
