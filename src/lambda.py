import json
import logging
from urllib.parse import unquote_plus

import boto3

import crypter

s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
DYNAMO_TABLE_NAME = 'hashes'

hashes = {
    'SHA256': crypter.hash_sha_256,
    'SHA3-256': crypter.hash_sha3_256
}

logger = logging.getLogger('crypter')
logger.setLevel(logging.INFO)

def handler(event, context):
    """ 
        Process uploaded files in S3 Bucket,
        generate SHA256 and SHA3-256 hashes,
        Put with S3 Object key and base64 encoded hashes in DynamoDB
    """

    for record in event['Records']:
        bucket = record.get('s3').get('bucket').get('name')

        key = unquote_plus(record.get('s3').get('object').get('key'))
        
        s3_obj = s3_client.get_object(Bucket=bucket, Key=key)
        obj_data = s3_obj.get('Body').read()
        logger.info(f'Loaded object {key} into memory.')

        db_filename = f'{bucket}_{key}'
        item_data = {
                'filename': {'S': db_filename},
            }
        for name, hasher in hashes.items():
            b64_hash = hasher(obj_data).decode('utf-8')
            logger.info(f'Generated Hash: {name}')
            item_data.update({
                name: {'S': b64_hash}
            })
        
        logger.info(f'Writing to DyanmoDB: {item_data}')
        dynamodb.put_item(
            TableName=DYNAMO_TABLE_NAME, 
            Item=item_data
        )