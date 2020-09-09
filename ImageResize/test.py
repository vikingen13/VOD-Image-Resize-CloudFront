'''
 # @ Author: Sébastien Grazzini
 # @ Create Time: 2020-07-30 17:08:03
 # @ Modified by: Sébastien Grazzini
 # @ Modified time: 2020-09-01 18:27:26
 # @ Description: This file is made to test the Resizer.py module
 '''

from PIL import Image
from Resizer import smartResize, resizeCenter
from aws_Helper import detectFacesAndTexts
from glob import glob


'''
To test the resizer module, first declare some bounding boxes.
Then open an image.
At last, run the resizer.

The bounding boxes can be taken from AWS rekognition test platform

ResizeCenter is used as a reference resize
'''

theImagePath = "testImages"

theResolutions = [(1080,1440),(800,600),(600,1080),(720,480)]


if __name__ == "__main__":

    for myImageFullName in glob(theImagePath+"/input/*.jpg"):
        myImageName = myImageFullName.split('/').pop()
        myImage = Image.open(myImageFullName)
        myDetectedFaces , myDetectedTexts = detectFacesAndTexts(myImage,aMinimalTextWidth=0.3,aMinimalTextHeight=0.08)
        for i in theResolutions:
            
            myOutputImage = smartResize(myImage,i[0],i[1],myDetectedFaces,myDetectedTexts)
            myOutputImage.save(theImagePath+"/output/"+myImageName+'.'+str(i[0])+'x'+str(i[1])+'.jpg')
            myOutputImage = resizeCenter(myImage,i[0],i[1])
            myOutputImage.save(theImagePath+"/output/"+myImageName+'.'+str(i[0])+'x'+str(i[1])+'center.'+'.jpg')
