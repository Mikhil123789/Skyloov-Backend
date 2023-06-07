# Start with the Python 3.9 image
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

##Setup python environments.
WORKDIR /app
RUN pip install -U pip
ADD ./requirements.txt /app/requirements.txt
RUN  pip install -r /app/requirements.txt 


ADD . /app
RUN chmod 775 -R /app

EXPOSE 8800

ENTRYPOINT ["/bin/sh", "/app/run.sh"]
