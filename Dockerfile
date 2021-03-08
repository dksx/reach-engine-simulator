FROM ubuntu:18.04
MAINTAINER dksx
WORKDIR /app/
COPY app/ /app/
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-pip python3.6-dev \
 && python3 -m pip install --upgrade pip setuptools wheel boto3 \
 && python3 -m pip install --upgrade uwsgi Flask \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get purge -y --auto-remove gcc python3-pip

ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]
