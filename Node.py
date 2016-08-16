'''

Node class

specialValue: math.inf if that node is a trap
start: the start Node
exit: the exit Node

'''
class Node:
    fee = 0
    specialValue = 0

    gValue = 0
    fValue = 0;
    
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        
    def GenerateChildren(self):
        tempX = self.x
        tempY = self.y
        retList = []
        
        tempX += 1
        if tempX <= 19:
            tempNode = Node(tempX, self.y)
            retList.append(tempNode)
            
        tempX -= 2
        if tempX >= 0:
            tempNode = Node(tempX, self.y)
            retList.append(tempNode)
        
        tempY += 1
        if tempY <= 19:
            tempNode = Node(self.x, tempY)
            retList.append(tempNode)
            
        tempY -= 2
        if tempY >= 0:
            tempNode = Node(self.x, tempY)
            retList.append(tempNode)
        
        return retList
    
    def PrettyStringNode(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'
