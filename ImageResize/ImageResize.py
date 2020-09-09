import json
import os
import aws_Helper
import Resizer
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """If this lambda is executed, it means that the resized image is not already present in the bucket
       The lambda get the size in the path and resize the original image
       If the original image is not present, we send a 404 error
        """

    try:
        #first we get the original image name and the size
        #as a reminder, the call is something like /WIDTHxHEIGHT/imgname

        #first of all, we log the event
        logger.info(event)

        myImageName = event['pathParameters']['filename']
        mySize = event['pathParameters']['size']
        logger.info('Size to process: '+mySize)
        
        if "ALLOWEDRESOLUTION" in os.environ:
            logger.info('allowed resolution activated')
            if mySize not in os.environ['ALLOWEDRESOLUTION']:
                logger.info('Resolution is not allowed, return 403 error')
                return {
                'statusCode': 403,
                'body': "resolution not allowed"
             }

        myTargetWidth,myTargetHeight = mySize.split('x')
        myOutputPath =mySize

        #we get the image from S3
        myOriginalImage = aws_Helper.getImageFromBucket(os.environ['BUCKET'],myImageName)

        if event['resource'].find('center') != -1 :
            myResizedImage = Resizer.resizeCenter(myOriginalImage,int(myTargetWidth),int(myTargetHeight))
            myOutputPath = 'center/'+myOutputPath

        else :
            #we analyze the image
            myDetectedFaces , myDetectedTexts = aws_Helper.detectFacesAndTexts(myOriginalImage,aMinimalTextWidth=0.3,aMinimalTextHeight=0.08)

            #we resize the image
            myResizedImage = Resizer.smartResize(myOriginalImage,int(myTargetWidth),int(myTargetHeight),myDetectedFaces,myDetectedTexts)
        
        #we write the image
        myImagePath = aws_Helper.putImageInBucket(myResizedImage,os.environ['BUCKET'],myOutputPath,myImageName)

        #we redirect to the stored image
        image_s3_url = os.environ['URL']+'/'+myImagePath

        myResponse = {}
        myResponse["statusCode"]=301
        myResponse["headers"]={'Location': image_s3_url}
        myResponse["body"]=json.dumps({})
        
        logger.info(myResponse)
        return myResponse

    except ClientError as ex:
        #if the original image cannot be found, we return a 404 error
        if ex.response['Error']['Code'] == 'NoSuchKey':
            logger.info('The image to resize does not exist')
            return {
            'statusCode': 404,
            'body': "Image not found"
            }  
            
        else:
            raise ex

    except Exception as e:
        #if anything goes wrong, we return an error that will be mapped by API GW
        raise Exception("[NOTFOUND] "+str(e))