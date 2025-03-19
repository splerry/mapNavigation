import csv
from inspect import _empty
import sys
import time
from operator import itemgetter
from queue import PriorityQueue

drivingFile = []
straightLineFile = []

with open("driving.csv", 'r') as drivingcsv:
    drivingreader = csv.reader(drivingcsv)
    for row in drivingreader:
        drivingFile.append(row)
with open("straightline.csv", 'r') as straightlinecsv:
    straightlinereader = csv.reader(straightlinecsv)
    for row in straightlinereader:
        straightLineFile.append(row)


class map:

    class mapNode:
        #initializes one state on the map: state:= name of state represented by node, adj:= list of states adjacent to this state and their distance, h:= heuristic of state relative to chosen destination
        def __init__(self, state = "", adj = [], parent = None, h = None):
            self.state = state
            self.adj = adj
            self.parent = parent
            self.h = h
        def __str__(self):
            pass

        def __repr__(self):
            return str(self)
    
    #intitializes the search: start:= starting state, end:= destination state
    def __init__(self, start = "None", end = "None"):
        self.start = start
        self.end = end
        self.history = []
        self.states = []
        stateList = []
        kj = 0

        #using given .csv file for states and distances, initializes the map
        for row in drivingFile:
            if kj == 0:
                stateList = row
                kj = 1
            else:
                temp = []
                for col in row:
                    if col != "-1" and col != "0" and col != row[0]:
                        temp.append((stateList[row.index(col)], int(col)))
                node = map.mapNode(row[0], temp)
                self.states.append(node)
                #print("Added state " + node.state)
    
    #prints name of state of given map node
    def mapPrint(self):
        for state in self.states:
            print(state.state)
            print(state.adj)

    #given state name as string, returns the map node representing that state
    def findOnMap(self, GoalState):
        for state in self.states:
            if state.state == GoalState:
                return state
    

    def pathPrint(self, path):
        for state in path:
            print(state.state)
        pass

    def fun(self, val):
        return val[1]
    
    #uses a greedy best-first-search algorithm to find 'best' path. Locally optimal, but may not be objectively optimal
    def BFSnav(self):
        sldata = self.processStraightLine()
        path = {self.start : (None, 0)}
        queue = []
        queue.append((0, 0, self.start))
        startNode = self.findOnMap(self.start)
        startNode.h = 0
        visited = []
        visited.append(self.start)


        while queue:
            current = queue.pop()
            currentG = current[1]
            current = self.findOnMap(current[2])

            current.h = self.findInSldata(sldata, current.state, self.end)

            if current.state == self.end:
                return path
            
            if current.state != self.start:
                visited.append(current.state)
            
            for state in current.adj:
                tempNode = self.findOnMap(state[0])
                
                if tempNode.state not in visited:
                    tempNode.parent = current
                    tempNode.h = self.findInSldata(sldata, tempNode.state, self.end)
                    if tempNode.state not in path or path[tempNode.state][1] > currentG + state[1]:
                        path[tempNode.state] = (current.state, state[1])
                    queue.append((tempNode.h, currentG + state[1], tempNode.state))
            queue.sort(reverse=True, key=itemgetter(0))
        
        return None

    def pathCreate(self, path):
        temp = []
        goal = self.end
        while goal:
            #print(temp)
            temp.append(goal)
            goal = path[goal][0]
        temp.reverse()
        return temp
    
    def pathCost(self, path):
        cost = 0
        for i in range (0, len(path) - 1):
            current = self.findOnMap(path[i])
            for state in current.adj:
                if state[0] == path[i + 1]:
                    cost = cost + state[1]
                    break
        return cost

    #Uses an A* algorithm to find the best path. May not be locally optimal, but will be objectively optimal
    def testAstar(self):
        path = {self.start : (None, 0)}
        queue = []
        queue.append((0, 0, self.start))
        while queue:
            current = queue.pop()
            currG = current[1]
            current = self.findOnMap(current[2])

            if current.state == self.end:
                return path
            else:
                for state in current.adj:
                    tempNode = self.findOnMap(state[0])
                    tempG = state[1] + currG
                    tempF = tempG + tempNode.h
                    tempNode.parent = current
                    if state[0] not in path or tempG < path[state[0]][1]:
                        path[state[0]] = (current.state, tempG)
                        queue.append((tempF, tempG, state[0]))
                        queue.sort(reverse=True, key=itemgetter(0))
        return None


    def processStraightLine(self):
        file = straightLineFile
        straightlineData = {}
        stateOrder = []
        i = 0
        for data in file:
            if i == 0:
                stateOrder = data
                i = 1
            else:
                temp = []
                for i in range(1, len(data)):
                    temp.append((stateOrder[i], data[i]))
                straightlineData[data[0]] = temp

        return straightlineData

    def findInSldata(self, sldata, state, request):
        for entry in sldata[state]:
            if entry[0] == request:
                return int(entry[1])


    def astarPrint(self, astarList):
        list = astarList
        for entry in list:
            print(entry[0].state)
            print(entry[1])
    
    def expandedNodes(self, path):
        temp = []
        for value in path.keys():
            if value is not None and value not in temp:
                temp.append(value)
        return len(temp)



if __name__ == "__main__":
    if len(sys.argv) == 3:
        start = sys.argv[1]
        end = sys.argv[2]

        testMapArg = map(start, end)

        testMapArg = map(start, end)
        print("Initial state: " + start)
        print("Goal state: " + end)
        print("")
        if testMapArg.findOnMap(start) in testMapArg.states and testMapArg.findOnMap(end) in testMapArg.states:
            start_time = time.time()
            testMapBFS = map(start, end)
            tempDicBFS = testMapBFS.BFSnav()
            end_time = time.time()
            if tempDicBFS is None:
                print("Greedy Best First Search:")
                print("NO SOLUTION FOUND")
                print("Number of stops on a path: 0")
                print("Execution time: " + start_time - end_time())
                print("Complete path cost: 0")
            else:
                tempNodesBFS = testMapBFS.expandedNodes(tempDicBFS)
                tempListBFS = testMapBFS.pathCreate(tempDicBFS)
                end_time = time.time()
                print("Greedy Best First Search:")
                print("Solution: " + ', '.join(tempListBFS))
                print("Number of expanded nodes: " + str(tempNodesBFS))
                print("Number of stops on path: " + str(len(tempListBFS)))
                print("Execution time: " + str(end_time - start_time))
                print("Complete path cost: " + str(testMapBFS.pathCost(tempListBFS)))
                print("")

            start_time = time.time()
            testMapAS = map(start, end)
            sldataAS = testMapAS.processStraightLine()
            for state in testMapAS.states:
                state.h = testMapAS.findInSldata(sldataAS, state.state, testMapAS.end)
            tempDicAS = testMapAS.testAstar()
            end_time = time.time()
            if tempDicAS is None:
                print("A* Search:")
                print("NO SOLUTION FOUND")
                print("Number of stops on a path: 0") 
                print("Execution time: " + str(end_time - start_time))
                print("Complete path cost: 0")
            else:
                tempNodesAS = testMapAS.expandedNodes(tempDicAS)
                tempListAS = testMapAS.pathCreate(tempDicAS)
                end_time = time.time()
                print("A* Search:")
                print("Solution: " + ', '.join(tempListAS))
                print("Number of expanded nodes: " + str(testMapAS.expandedNodes(tempDicAS)))
                print("Number of stops on path: " + str(len(tempListAS)))
                print("Execution time: " + str(time.time() - start_time))
                print("Complete path cost: " + str(testMapAS.pathCost(tempListAS)))
        else:
                print("Greedy Best First Search:")
                print("NO SOLUTION FOUND")
                print("Number of stops on a path: N/A")
                print("Execution time: 0.00")
                print("Complete path cost: N/A")
                print("")
                print("A* Search:")
                print("NO SOLUTION FOUND")
                print("Number of stops on a path: N/A")
                print("Execution time: 0.00")
                print("Complete path cost: N/A")
    else:
        print("ERROR: Not enough or too many input arguments.")
