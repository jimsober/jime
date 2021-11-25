FROM python:3-slim

ENV TERM=xterm-256color
ENV TZ="MST"

WORKDIR /usr/src/app

COPY jime.* .

CMD [ "python", "./jime.py" ]
