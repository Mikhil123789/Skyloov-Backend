# Start with the Python 3.9 image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/bin/sh", "/app/run.sh"]
