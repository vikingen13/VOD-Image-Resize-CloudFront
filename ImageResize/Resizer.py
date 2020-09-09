'''
 # @ Author: Sébastien Grazzini
 # @ Create Time: 2020-07-30 16:40:18
 # @ Modified by: Sébastien Grazzini
 # @ Modified time: 2020-09-01 17:57:10
 # @ Description: This module contain a method to resize smartly
 '''

import os
from PIL import Image, ImageDraw
from Rectangle import Rectangle
import logging
logger = logging.getLogger()    

#this method resize an image
#it will crop the image but will try to preserve zone of interest thanks to AI
# Zone of interest are texts and faces
# first we check if the cropped image can contain all zone of interest
# if not, we check if we can embed the Texts
# if not, we focus on faces
# if not, we return the image cropped from center
def smartResize(anImageInput, aWidth, aHeight, aDetectedFaceBoundingBoxes,aDetectedTextBoundingBoxes):

    # important note
    # The algorithm starts to crop the image to the correct ratio in its original size
    # once the crop is done, we resize the image to the target size
    logger.info("Start resize process")

    myOriginalWidth, myOriginalHeight = anImageInput.size

    #first of all, lets concatenate the 2 lists
    myInterestBoundingBoxes = aDetectedFaceBoundingBoxes+aDetectedTextBoundingBoxes
    myCropBox = Rectangle(0,0,1,1)

    myTargetImage = anImageInput
    
    #first of all, we calculate image ratios
    myTargetRatio = aWidth / float(aHeight)
    myOriginalRatio = myOriginalWidth/float(myOriginalHeight)

    #from the image aspect ratio, we get the target rectangle width and height in relative values
    #the important point is to understand that we will never crop the width and the height but only one of the two values

    if myTargetRatio > myOriginalRatio:
        myCropBox = Rectangle(0,0,1,myOriginalWidth/myTargetRatio/myOriginalHeight)
    elif myTargetRatio < myOriginalRatio:
        myCropBox = Rectangle(0,0,myOriginalHeight*myTargetRatio/myOriginalWidth,1)

    #at this point, the problem to solve is to maximize the position of the cropbox to embed the maximum number of interesting elements

    #are we able to embed everything?
    myVirtualRectangle = Rectangle.fromBoundingBoxes(myInterestBoundingBoxes)

    if myCropBox.canContains(myVirtualRectangle):
        logger.info("Nice, all faces and texts can be embedded")
        #bingo, everything can be embedded so we just need to put the rectangle at the right place
        myCropBox.moveCenter(myVirtualRectangle.getCenter())
    
    else:
        #we try with the faces only
        myVirtualRectangle = Rectangle.fromBoundingBoxes(aDetectedFaceBoundingBoxes)
        if myCropBox.canContains(myVirtualRectangle):
            #bingo, all faces can be embedded
            logger.info("Only the faces can be embedded")
            myCropBox.moveCenter(myVirtualRectangle.getCenter())

        else:
            #we try with the texts only
            myVirtualRectangle = Rectangle.fromBoundingBoxes(aDetectedTextBoundingBoxes)
            if myCropBox.canContains(myVirtualRectangle):
                #bingo, all texts can be embedded
                logger.info("Only the texts can be embedded")
                myCropBox.moveCenter(myVirtualRectangle.getCenter())

            else:
                #too bad, let's crop using the center of the image
                logger.info("Too bad, nothing can be embedded")
                myCropBox.moveCenter( (0.5,0.5) )

    #at this point, we have a rectangle on which we can crop
    #warning: The rectangle is a relative rectangle that we need to translate in absolute values

    myLeftCrop =   myCropBox.theLeft*myOriginalWidth
    myRightCrop =  (myCropBox.theLeft+myCropBox.theWidth) *myOriginalWidth
    myTopCrop =    myCropBox.theTop * myOriginalHeight
    myBottomCrop = (myCropBox.theTop+myCropBox.theHeight) *myOriginalHeight

    myTargetImage = myTargetImage.crop( (myLeftCrop,myTopCrop,myRightCrop,myBottomCrop) )

    #now we have a cropped image with the correct proportions and we just need to resize the image    
    myTargetImage = myTargetImage.resize((aWidth,aHeight), Image.ANTIALIAS)        

    logger.info("End of resize process")
    return myTargetImage


def resizeCenter(anImageInput, aWidth, aHeight):
    ''''This function resize an image. If the aspect ratio is different than the original,
        the cropping is done using the center of the image
    Parameters:
    anImage(PIL image): theImage to resize
    width (int): the new width
    height (int): the new height
    Returns: the resized image
    '''

    myTargetImage = anImageInput
    #first we crop the image
    myTargetRatio = aWidth / float(aHeight)
    myOriginalWidth, myOriginalHeight = anImageInput.size
    myOriginalRatio = myOriginalWidth/float(myOriginalHeight)

    myCropBox = Rectangle(0,0,1,1)

    if myTargetRatio > myOriginalRatio:
        myCropBox = Rectangle(0,0,1,myOriginalWidth/myTargetRatio/myOriginalHeight)
    elif myTargetRatio < myOriginalRatio:
        myCropBox = Rectangle(0,0,myOriginalHeight*myTargetRatio/myOriginalWidth,1)

    #too bad, let's crop using the center of the image
    myCropBox.moveCenter( (0.5,0.5) )

    #warning: The rectangle is a relative rectangle that we need to translate in absolute values

    myLeftCrop =   myCropBox.theLeft*myOriginalWidth
    myRightCrop =  (myCropBox.theLeft+myCropBox.theWidth) *myOriginalWidth
    myTopCrop =    myCropBox.theTop * myOriginalHeight
    myBottomCrop = (myCropBox.theTop+myCropBox.theHeight) *myOriginalHeight

    myTargetImage = myTargetImage.crop( (myLeftCrop,myTopCrop,myRightCrop,myBottomCrop) )

    #now we have a cropped image with the correct proportions and we just need to resize the image    
    myTargetImage = myTargetImage.resize((aWidth,aHeight), Image.ANTIALIAS)        

    return myTargetImage