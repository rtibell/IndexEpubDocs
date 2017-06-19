from __future__ import print_function

import json
import urllib
import boto3

import ReadEpub
print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        #response = s3.get_object(Bucket=bucket, Key=key)
        #print("CONTENT TYPE: " + response['ContentType'])
	file_name = "/tmp/{}".format(key)
	print("Filename={}".format(file_name))
        #return response['ContentType']
	s3.download_file(Bucket=bucket, Key=key, Filename=file_name)
	ReadEpub.read_book(file_name)
        return key
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

