'''

BuildMaze class

specialList: List of nodes that are traps or that contain fees.
start: Starting position for the Agent
exit: Exit position for the Agent

'''
import math
from Node import Node

class BuildMaze:
    def __init__(self):
        self.specialList = []

        with open('input2.txt', 'r') as f:
            startPos = f.readline()
            exitPos = f.readline()
            sandsPos = f.readline()
            spiderPos = f.readline()
            feePos = f.readline()

        temp = ParseCoordinates(startPos)    
        for coordinate in temp:
            self.start = Node(coordinate.x, coordinate.y)

        temp = ParseCoordinates(exitPos)
        for coordinate in temp:
            self.exit = Node(coordinate.x, coordinate.y)            

        temp = ParseCoordinates(sandsPos)
        for coordinate in temp:
            tempNode = Node(coordinate.x, coordinate.y)
            tempNode.specialValue = math.inf
            self.specialList.append(tempNode)

        temp = ParseCoordinates(spiderPos)
        temp = BuildSpiderNets(temp)
        for coordinate in temp:
            tempNode = Node(coordinate.x, coordinate.y)
            tempNode.specialValue = math.inf
            self.specialList.append(tempNode)

        temp = ParseFee(feePos)
        for fee, node in temp:
            node.fee = fee
            self.specialList.append(node)
def ParseCoordinates(coordinates):
    coordinates = coordinates.split()
    tempNodeList = []
    for item in coordinates:
        temp = list(map(int, item.strip('()').split(',')))
        tempNodeList.append(Node(temp[0], temp[1]))
    
    return tempNodeList

def ParseFee(feePos):
    feePos = feePos.split()
    feeList = []
    
    for item in feePos:
        item = item.split(':')
        tempList = ParseCoordinates(item[1])
        tempList.insert(0, int(item[0]))
        feeList.append(tempList)

    return feeList

def BuildSpiderNets(nodeList):
    spiderNetList = nodeList[:]
    for node in nodeList:
        retNodes = node.GenerateChildren()
        for item in retNodes:
            spiderNetList.append(item)
    
    return spiderNetList