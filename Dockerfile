FROM ubuntu:18.04
MAINTAINER dksx
WORKDIR /app/
COPY app/ /app/
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-pip python3.6-dev \
 && python3 -m pip install --upgrade pip setuptools wheel \
 && python3 -m pip install --upgrade boto3 uwsgi Flask \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get purge -y --auto-remove gcc python3-pip

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]
