import json
import os
import aws_Helper
import Resizer
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

resolutions = ['1080x1440','800x600','600x1080','720x480']

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

        for myRecord in event['Records']:

            myObjectName = myRecord['s3']['object']['key']
            #we get the image from S3
            myOriginalImage = aws_Helper.getImageFromBucket(myRecord['s3']['bucket']['name'],myObjectName)
            
            myImageName = myObjectName.split('/').pop()

            for mySize in resolutions:
                
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

                myResizedImageCentered = Resizer.resizeCenter(myOriginalImage,int(myTargetWidth),int(myTargetHeight))
                myOutputPathCentered = 'center/'+myOutputPath

                #we analyze the image
                myDetectedFaces , myDetectedTexts = aws_Helper.detectFacesAndTexts(myOriginalImage,aMinimalTextWidth=0.3,aMinimalTextHeight=0.08)

                #we resize the image
                myResizedImage = Resizer.smartResize(myOriginalImage,int(myTargetWidth),int(myTargetHeight),myDetectedFaces,myDetectedTexts)
                
                #we write the images
                myImagePathCenter = aws_Helper.putImageInBucket(myResizedImageCentered,os.environ['BUCKET'],myOutputPathCentered,myImageName)
                myImagePath = aws_Helper.putImageInBucket(myResizedImage,os.environ['BUCKET'],myOutputPath,myImageName)

            #we get the json from S3
            myPicList = aws_Helper.getJsonFromBucket(os.environ['BUCKET'],"picList.json")

            #we update the json
            myPicList['pics'].append(myImageName)
            aws_Helper.putJsonInBucket(myPicList,os.environ['BUCKET'],"picList.json")

        logger.info("end")
        return 200

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