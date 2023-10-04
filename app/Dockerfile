FROM ubuntu:22.04

RUN apt-get install -y libpq-dev

# Install python and dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.10 && \
    apt-get install -y python3-pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "app.py" ]
