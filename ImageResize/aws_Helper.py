'''
 # @ Author: Sébastien Grazzini
 # @ Create Time: 2020-07-30 16:14:37
 # @ Modified by: Sébastien Grazzini
 # @ Modified time: 2020-07-30 16:16:31
 # @ Description: This module is used to perform operations on AWS modules
 '''

import os
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from PIL import Image, ImageDraw

"""
This function return a PIL.Image object from a S3 bucket
The image shall be at the root of the S3
"""
def getImageFromBucket(aBucketName,anImageName):
    myS3 = boto3.resource('s3')
    myS3Object = myS3.Object(
        bucket_name=aBucketName,
        key=anImageName,
    )
    
    myS3ObjectBody = myS3Object.get()['Body'].read()

    myImage = Image.open( BytesIO(myS3ObjectBody) )
    return myImage

"""
this function stores a JPEG PIL.image object in a S3 bucket.
aPath can be given
"""
def putImageInBucket(anImage,aBucketName,aPath,anImageName):
    myS3 = boto3.resource('s3')
    myS3Object = myS3.Object(
        bucket_name=aBucketName,
        key=aPath+'/'+anImageName,
    )

    myBuffer = BytesIO()
    anImage.save(myBuffer, 'JPEG')
    myBuffer.seek(0)

    myS3Object.put(Body=myBuffer, ContentType='image/jpeg')

    return aPath+'/'+anImageName

"""
this method uses the rekognition features to detect faces and big texts in an image
Parameters:
  anImage -> PIL.Image to analyse
  aMinimalTextWidth -> the minimal size of text to detect expressed in% of the image size (50% per default)
  aMinimalTextHeight -> the minimal size of text to detect expressed in% of the image size (10% per default)
it returns 2 list containing the faces and text boxes, with relative coordinates (relative to the image)
for example, if the image size is 700px and the coordinate is at 350, relative will be 0.5 (350/700)
"""
def detectFacesAndTexts(anImage, aMinimalTextWidth = 0.5, aMinimalTextHeight = 0.1, aMinimalFaceWidth = 0.05, aMinimalFaceHeight = 0.05):
    myAIClient = boto3.client('rekognition')
    #Call DetectFaces
    myTMPBuffer = BytesIO()
    anImage.save(myTMPBuffer, 'JPEG')
    myTMPBuffer.seek(0) 
    myFaces = myAIClient.detect_faces(Image={'Bytes': myTMPBuffer.getvalue()},
        Attributes=['DEFAULT'])
    
    myDetectedFacesBoundingBoxes = [(i['BoundingBox']['Left'],i['BoundingBox']['Top'],i['BoundingBox']['Width'],i['BoundingBox']['Height']) for i in myFaces['FaceDetails'] if i['BoundingBox']['Width']>aMinimalFaceWidth and i['BoundingBox']['Height']>aMinimalFaceHeight]
    
    #call detect text
    myTMPBuffer.seek(0)
    myTexts = myAIClient.detect_text(Image={'Bytes': myTMPBuffer.getvalue()})

    # we keep the text with size > min text size% of the image size
    myDetectedTexts = [i for i in myTexts['TextDetections'] if i['Geometry']['BoundingBox']['Width']>aMinimalTextWidth and i['Geometry']['BoundingBox']['Height']>aMinimalTextHeight]
    myDetectedTextsBoundingBoxes = [(i['Geometry']['BoundingBox']['Left'],i['Geometry']['BoundingBox']['Top'],i['Geometry']['BoundingBox']['Width'],i['Geometry']['BoundingBox']['Height']) for i in myDetectedTexts if i['Type']=='LINE' ]

    return (myDetectedFacesBoundingBoxes,myDetectedTextsBoundingBoxes)
