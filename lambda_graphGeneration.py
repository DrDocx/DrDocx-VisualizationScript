import json
import boto3

_decodedJson = ""

def lambda_handler(event, context):
    ingestDataFile(event)

def ingestDataFile(event):
    global _decodedJson
    
    s3 = boto3.client('s3')

    #print("Event Full: ", event)
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = (record['s3']['object']['key'])
    tmpkey = key.replace('/', '')
    #print(tmpkey)

    _file = s3.get_object(Bucket = 'doctordocx-patientdata', Key = tmpkey)
    _data = _file['Body'].read()
    _decodedJson = json.loads(_data)
    #print(_decodedJson)
    
    #_le = _s3.get_object(Bucket = _bucket)
    #_dataStream = bucket.objects.all()['Patient_Aaren.json']