from math import cos,sin,radians

from numpy import poly
class Transform:
    @staticmethod
    def rotate(x,y,angle):
        theta = radians(angle)
        return(
                x * cos(theta) - y * sin(theta),
                x * sin(theta) + y * cos(theta)
                )

class pointTools:
    def __init__(self) -> None:
        pass
    
    def isInBetween(self,y,y1,y2):
        if (y1>y2 and y1 >= y > y2) or (y2>y1 and y2 >= y > y1):
            return True
        return False

    def getIntersection(self,p,a,b):
        m = (b[1]-a[1]) / (b[0]-a[0])
        y = p[1]
        x = ((y-a[1])/m)+a[0]
        return (x,y)
    
    def containedIn(self,polygon, point):
        count = 0
        for i in range(len(polygon)):
            a = polygon[i - 1]
            b = polygon[i]
            
            if (a[1] != b[1] and self.isInBetween(point[1],a[1], b[1])):
                intersection = self.getIntersection(point,a,b)
                if intersection[0] >= point[0]:
                    count += 1

        if count % 2 == 0:
            return False
        return True

