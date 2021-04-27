import json
import os
import boto3
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """If this lambda is executed, it means that the resized image has been stored in the website bucket """

    try:
        #here we just need to store the image name in the dynamoDB table

        #first of all, we log the event
        logger.info(event)
        myClient = boto3.client('dynamodb')

        for myRecord in event['Records']:

            myObjectName = myRecord['s3']['object']['key']
            
            myImageName = myObjectName.split('/').pop()
                
            #we write the image name in dynamoDB
            myResponse = myClient.put_item(
                TableName=os.environ['DBTABLE'],
                Item={
                'Image': {'S':myImageName}})

        logger.info("end")
        return 200

    except ClientError as ex:
        raise ex

    except Exception as e:
        #if anything goes wrong, we return an error that will be mapped by API GW
        raise Exception("[NOTFOUND] "+str(e))