
'''
Brian Orbegoso

July 25, 2016

Entry point: maze()

'''
import math
import itertools
from Node import Node
from BuildMaze import BuildMaze

def maze():
    x = BuildMaze()

    start = x.start
    exit = x.exit
    
    cost, master_path = AStar(start, exit, x.specialList)
    
    tempCost = 0
    acumulate_cost = 0
    final_path = []
    for index, node in enumerate(master_path):
        if node is None:
            tempStart = master_path[index - 1]
            tempExit = master_path[index + 1]
            tempStart.gValue = 0
            tempExit.gValue = 0
            tempExit.specialValue = 0
            tempCost, tempPath = AStar(tempStart, tempExit, x.specialList)
            final_path.append(tempPath[1:])
            # Don't count the fee twice
            tempCost -= tempStart.fee
            # Don't count the same step twice
            tempCost -= 1
            acumulate_cost += tempCost

    # Replace every occurence of None in the master_path with the backtracked path the Agent traveled
    tempCount = 0
    master_list = [[]]
    for item in master_path:
        if item is not None:
            master_list[tempCount].append(item)
        elif item is None:
            tempCount += 1
            master_list.append(list())

    
    all_list = interleave(master_list, final_path)
    all_list = list(itertools.chain.from_iterable(all_list))

    # Append the exit that was left out in AStar previously
    all_list.append(exit)
    
    WriteReport(cost + acumulate_cost, len(all_list) - 1, all_list)

'''
AStar()

In: start: The starting Node for the Agent
    exit:  The exit Node for the Agent
    specialList: The list of Nodes that have a fee or are a trap

Out: cost: The amount of steps taken plus the fees incurred. The total amount of money spent.
     path: A list of the Nodes  traveled by the Agent, excluding the exit Node.
'''
def AStar(start, exit, specialList):
    closedList = []
    openList = []
    path = []
    cost = 0

    openList.append(start)

    # Loop while openList is not empty
    while openList:
        currentNode = openList[0]
        #currentitem = openList[0]
        
        # Remove the first item from openList
        openList.pop(0)
        
        # Check if the Agent 'jumped' from the previous node to the current node
        if closedList and not Neighbors(currentNode, closedList[-1]):
            path.append(None)
               
        path.append(currentNode)

        cost += currentNode.fee

        children = currentNode.GenerateChildren()
                   
        for child in children:
            # Initialize all the children with their fees and specialValues
            isinList, member = inSpecialList(child, specialList)
            if isinList:
                child.fee = member.fee
                child.specialValue = member.specialValue
            
            new_cost = currentNode.gValue + child.fee + 1

            # Check if the child is the exit
            if SameLocation(child, exit):
                # Leave the exit out of the path for now
                # path.append(child)
                return cost + child.fee + 1, path
                
            if inList(child, closedList):
                continue                               
                
            if inList(child, openList):                       
                if currentNode.gValue > new_cost:
                    child.gValue = new_cost
                    child.fValue = f(child, exit, new_cost)
                    openList.insert(0, child)
            else:
                child.gValue = new_cost
                # Not appended, current node's children would be a tiebreaker if same g-value as other nodes
                child.fValue = f(child, exit, new_cost)
                openList.insert(0, child)

        cost += 1
                
        closedList.append(currentNode)

        # Sort the openList by each item's f-value in increasing order. Note: sorted() is a stable sort.
        openList = sorted(openList, key=lambda k: k.fValue, reverse=False)

    return _,_


'''
Heuristic functions

'''

def f(node, exit, cost):
    return g(node) + h(node, exit)
    
# Number of nodes from current position to exit
def h(node, exit):
    return ManhattanDistance(node, exit) + node.specialValue
    
# Amount of money spent so far
def g(node):
    # current.gValue + node.fee + 1
    return node.gValue
    
def ManhattanDistance(firstNode, secondNode):
    x = abs(firstNode.x - secondNode.x)
    y = abs(firstNode.y - secondNode.y)
     
    return 1 * (x + y)


'''

Helper functions

'''

def interleave(l1, l2):
    '''
    Interleave two lists.

    http://stackoverflow.com/a/29566946/3423701
    '''
    iter1 = iter(l1)
    iter2 = iter(l2)

    while True:
        try:
            if iter1 != None:
                yield next(iter1)
        except StopIteration:
            iter1 = None
        try:
            if iter2 != None:
                yield next(iter2)
        except StopIteration:
            iter2 = None
        if iter1 == None and iter2 == None:
            raise StopIteration()


def SameLocation(firstNode, secondNode):
    '''
    Determines if two nodes are at the same location
    '''
    if firstNode == None or secondNode == None:
        return False
    if firstNode.x == secondNode.x and firstNode.y == secondNode.y:
        return True
    else:
        return False

def inSpecialList(node, specialList):
    for member in specialList:
        if SameLocation(node, member):
            return True, member
    return False, None

def inList(node, queuelist):
    for member in queuelist:
        if SameLocation(node, member):
            return True        
    return False

def Neighbors(first, second):
    x = abs(first.x - second.x)
    y = abs(first.y - second.y)
    
    if x + y >= 2:
        return False
    else:
        return True

def WriteReport(cost, steps, path):
    with open('output.txt', 'w') as f:
        f.write('Total cost: $'+ str(cost) + '\n')
        f.write('Steps taken: ' + str(steps) + '\n')
        f.write('Path taken: ')

        print('Total cost: $' + str(cost))
        print('Steps taken: ' + str(steps))
        print('Path taken: ', end='')
    
        temp = ''
        for node in path:
            temp += node.PrettyStringNode() + ' '
        f.write(temp)
        print(temp)


if __name__ == '__main__':
    maze()

