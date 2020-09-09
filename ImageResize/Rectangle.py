'''
 # @ Author: Sébastien Grazzini
 # @ Create Time: 2020-09-01 14:31:33
 # @ Modified by: Sébastien Grazzini
 # @ Modified time: 2020-09-01 14:55:55
 # @ Description: Contains a class to manipulate 2D rectangles on a picture 
 '''

class Rectangle(object):

    def __init__(self,aLeft,aTop,aWidth,aHeight):
        ''''Create a rectangle object in a space
        All values are given as a ratio between the coordinate and the absolute value.
        For example, if the total space is 100x100 and the rectangle left point is at 50, the value will be 0.5 (50/100)
        This method allow to locate the rectangle in space
        Parameters:
        aLeft (float): a Left Coordinate in the space
        aTop (float): a top Coordinate in the space
        aWidth (float): width of the rectangle
        aHeight (float): the Height of the rectangle
        '''
        self.theLeft = aLeft
        self.theTop = aTop
        self.theWidth = aWidth
        self.theHeight = aHeight

    @classmethod
    def fromBoundingBoxes(cls,aBoundingBoxList):
        ''''This method create a Rectangle embedding all boundingboxes in the boundingBoxList list
        as a class method, it can be used to construct a new rectangle
        Parameters:
        aBoundingBoxList(array of Left,Top,Width and Height tuples)
        Returns: a Rectangle. If bounding box list is empty, we return centered rectangle with a size of 0 
        '''

        def getLeft(aBoundingBox):
            return aBoundingBox[0]
        def getTop(aBoundingBox):
            return aBoundingBox[1]
        def getRight(aBoundingBox):
            return(aBoundingBox[0]+aBoundingBox[2])
        def getBottom(aBoundingBox):
            return(aBoundingBox[1]+aBoundingBox[3])

        if len(aBoundingBoxList)==0:
            return cls(0.5,0.5,0,0)
        myLeft = min(aBoundingBoxList,key=getLeft)[0]
        myTop = min(aBoundingBoxList,key=getTop)[1]

        myRightestBoundingBox = max(aBoundingBoxList,key=getRight)
        myRight = myRightestBoundingBox[0]+myRightestBoundingBox[2]

        myLowestBoundingBox = max(aBoundingBoxList,key=getBottom)
        myBottom = myLowestBoundingBox[1]+myLowestBoundingBox[3]

        return cls(myLeft,myTop,myRight-myLeft,myBottom-myTop)

    @property
    def theLeft(self):
        return self.__theLeft
    
    @theLeft.setter
    def theLeft(self,var):
        self.__theLeft = float(var)
    
    @property
    def theTop(self):
        return self.__theTop
    
    @theTop.setter
    def theTop(self,var):
        self.__theTop = float(var)

    @property
    def theWidth(self):
        return self.__theWidth
    
    @theWidth.setter
    def theWidth(self,var):
        self.__theWidth = float(var)

    @property
    def theHeight(self):
        return self.__theHeight
    
    @theHeight.setter
    def theHeight(self,var):
        self.__theHeight = float(var)

    def canContains(self,aRectangle):
        ''''Check if the rectangle in parameter can be contained within our rectangle object
        Note that it does not check if it is contained but if it can be contained
        Parameters:
        aRectangle (Rectangle): the rectangle to check
        Returns: True if the rectangle passed in parameter is contained in our rectangle
        False otherwise
        '''
        if aRectangle.theWidth < self.theWidth and aRectangle.theHeight < self.theHeight:
            return True
        else:
            return False

    def getCenter(self):
        ''''Return the center of a Rectangle
        Returns: a tuple containing the coordinates of the rectangle's center (left,top)
        '''
        return (self.theLeft+self.theWidth/2,self.theTop+self.theHeight/2)

    def moveCenter(self,aNewCoordinate):
        ''''move a Rectangle to a new coordinate so that it is as much centered as possible around the point in parameter
        Note that the moved rectangle will still be in the global frame so centering a rectangle around a point at the edge of the frame
        will result in a Rectangle embedding the center but not centered around this point
        Parameters:
        aNewCoordinate(float,float): Coordinate of the targeted center
        '''
        #first of all, we check if the new center is in the frame. If not, we put it in the frame
        aNewCoordinate = ( min( max(aNewCoordinate[0],0),1), min( max(aNewCoordinate[1],0),1) )

        #then we calculate the new coordinates
        #first we position the new left and top in the frame and then we adjust in case the rectangle is out of the frame
        self.theLeft = min( max(  aNewCoordinate[0]-self.theWidth/2 ,0) ,1)
        self.theTop = min( max(  aNewCoordinate[1]-self.theHeight/2 ,0) ,1)

        if self.theLeft + self.theWidth > 1:
            self.theLeft = 1 - self.theWidth
        if self.theTop + self.theHeight > 1:
            self.theTop = 1 - self.theHeight

