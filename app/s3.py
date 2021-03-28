import os
import sys
import uuid
import boto3.session as s3session
from botocore.exceptions import ClientError
from flask import Flask, request
import csv
import json
import random

ACCESS_KEY_AWS = ''
SECRET_KEY_AWS = ''
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

hashmap_ = dict()
with open('dcl.csv', 'r') as csvfile:
    data = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
    for i in data:
        hashmap_[i[1]] = i[4]

app = Flask(__name__)


#@cron(-1, -1, -1, -1, -1)
#def run_periodic_task(num):
#    x = dt.datetime.now()
#    print(x.strftime("%X"))

def upload_file(file_):
    file_name = 'strand.mp4'
    object_ = 'reach_engine'
    access_key = ACCESS_KEY_AWS
    secret_key = SECRET_KEY_AWS
    region = 'eu-north-1'
    bucket = ''
    object_name = f'{object_}/{file_}'
    session = s3session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)
    s3_client = session.client('s3', config=s3session.Config(signature_version='s3v4'))
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, Callback=ProgressPercentage(file_name))
        print('')
    except ClientError as e:
        print(e)

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self.bytes_sent = 0

    def __call__(self, byte_chunk):
            self.bytes_sent += byte_chunk
            percentage = (self.bytes_sent / self._size) * 100
            sys.stdout.write("\r * %s - %.2f%%" % (self._filename, percentage))
            sys.stdout.flush()

@app.route("/reachengine", methods=["POST", "GET"])
def log():
    #print("\n---- Request args ----\n")
    #print(request.args)
    print("\n\n---- Request data ----\n")
    print(f"{str(request.data, 'utf-8', 'ignore')}\n")
    #print("\n\n---- Request form ----\n")
    #print(request.form)
    #print("\n\n---- Request headers ----\n")
    #print(request.headers)
    #print("\n")
    return "", 200

@app.route("/reachengine/api/workflows/archive/<workflow_id>/start", methods=["POST"])
def reach_engine_archive(workflow_id):
    if request.method != 'POST':
        return '', 511
    try:
        print(f"{str(request.data, 'utf-8', 'ignore')}\n")
        uuid_ = str(uuid.uuid4())
        workflow_execution_id = uuid_.split('-')[-1]
        dcl_id = uuid_.split('-')[0]
        response = dict(workflowId=workflow_id, ArchiveId=dcl_id, Id=workflow_execution_id,
                            ExecutionStatus="EXECUTING", ErrorMessage="", PercentComplete="10")
        return response, 200
    except Exception as e:
        print(f'Exception - {e}')
        return dict(response=f'Error during execution - {e}'), 500

@app.route("/reachengine/api/workflows/<workflow_id>/start", methods=["POST"])
def reach_engine_restore(workflow_id):
    if request.method != 'POST':
        return '', 511
    try:
        payload = json.loads(str(request.data, 'utf-8', 'ignore'))
        print(str(request.data, 'utf-8', 'ignore'))
        dcl_id = payload["subject"].split(".")[1]
        filename = hashmap_.get(dcl_id)
        if filename is not None:
            if payload["exportFormat"] == "source":
                uuid_ = payload["arvatoUuid"]
                if(uuid_ and uuid_.strip()):
                    print(f"{uuid_}_{filename}")
                else:
                    print(f"{filename}")
            else:
                print(f"{filename}.mp4")
            workflow_execution_id = str(uuid.uuid4()).split('-')[-1]
            response = dict(workflowId=workflow_id, ArchiveId=dcl_id, Id=workflow_execution_id,
                                ExecutionStatus="EXECUTING", ErrorMessage="", PercentComplete="10")
            return response, 200
        else:
            upload_file(f"Reach_Engine_Error.ogx")
            workflow_execution_id = str(uuid.uuid4()).split('-')[-1]
            response = dict(workflowId=workflow_id, ArchiveId=dcl_id, Id=workflow_execution_id,
                                ExecutionStatus="EXECUTING", ErrorMessage="", PercentComplete="10")
            return response, 200
    except Exception as e:
        print(f'Exception - {e}')
        return dict(response=f'Error during execution - {e}'), 500

@app.route("/reachengine/api/workflows/executions/<execution_id>", methods=["GET"])
def execution_status(execution_id):
    if request.method != 'GET':
        return '', 511
    try:
        recount_ = random.randint(1, 4)
        if recount_ > 1:
            response = dict(Id=execution_id, Status="EXECUTING", ErrorMessage="", PercentComplete="10")
            return response, 200
        else:
            response = dict(Id=execution_id, Status="COMPLETED", ErrorMessage="", PercentComplete="100")
            return response, 200
    except Exception as e:
        print(f'Exception - {e}')
        return dict(response=f'Error during execution - {e}'), 500

@app.route("/reachengine/api/workflows/metadata/<dcl_id>", methods=["POST"])
def log_metadata(dcl_id):
    if request.method != 'POST':
        return '', 511
    print("\n\n---- Request data ----\n")
    print(f"{str(request.data, 'utf-8', 'ignore')}\n")
    return "", 200

@app.route('/<path:path>', methods=HTTP_METHODS)
def fallback(path=None):
    return '', 511


#if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0', port=8080)