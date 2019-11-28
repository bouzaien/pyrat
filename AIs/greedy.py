TEAM_NAME = "Greedy"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'


##################
# Useful imports #
##################

import heapq
from PIL import Image
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


heatMap = np.zeros((15, 21))
cheeseMap = np.zeros((15, 21))

#################################################################################
# Transforms a pair of locations into a move going from the first to the second #
#################################################################################

def locationsToMove (location1, location2) :
    # Depends on the difference
    difference = (location2[0] - location1[0], location2[1] - location1[1])
    if difference == (-1, 0) :
        return MOVE_LEFT
    elif difference == (1, 0) :
        return MOVE_RIGHT
    elif difference == (0, 1) :
        return MOVE_UP
    elif difference == (0, -1) :
        return MOVE_DOWN
    else :
        raise Exception("Invalid location provided")
    
##################################################################################################
# Dijkstra's algorithm to compute the shortest paths from the initial locations to all the nodes #
# Returns for each location the previous one that leads to the shortest path                     #
##################################################################################################

def dijkstra (mazeMap, initialLocation) :
    
    # We initialize the min-heap with the source node
    # Distances and routes are updated once the nodes are visited for the first time
    # The temporary values are stored in the min-heap
    minHeap = [(0, initialLocation, None)]
    distances = {}
    routes = {}
    
    # Main loop
    while len(minHeap) != 0 :
        (distance, location, predecessor) = heapq.heappop(minHeap)
        if location not in distances :
            distances[location] = distance
            routes[location] = predecessor
            for neighbor in mazeMap[location] :
                newDistanceToNeighbor = distance + mazeMap[location][neighbor]
                heapq.heappush(minHeap, (newDistanceToNeighbor, neighbor, location))
    
    # Result
    return (routes, distances)
    
###############################################################
# Takes as an input the result of Dijkstra's algorithm        #
# Returns the sequence of nodes from sourceNode to targetNode #
###############################################################

def routesToPath (routes, targetNode) :
    
    # Recursive reconstruction
    if not targetNode :
        return []
    elif targetNode in routes :
        return routesToPath(routes, routes[targetNode]) + [targetNode]
    else :
        raise Exception("Impossible to reach target")

###############################################################################
# Returns the sequence of moves in the maze associated to a path in the graph #
###############################################################################

def pathToMoves (path) :
    
    # Recursive reconstruction
    if len(path) <= 1 :
        return []
    else :
        return [locationsToMove(path[0], path[1])] + pathToMoves(path[1:])


###################################################
# Function that finds the closest piece of cheese #
###################################################

def findClosestPieceOfCheese (distances, piecesOfCheese) :
    
    # We return the cheese associated with the minimum distance
    distancesToCheese = {cheese : distances[cheese] for cheese in piecesOfCheese}
    return min(distancesToCheese, key=distancesToCheese.get)


def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :
    global heatMap
    global cheeseMap
    
    heatMap = np.zeros((mazeHeight, mazeWidth))
    cheeseMap = np.zeros((mazeHeight, mazeWidth))
    for cheese in piecesOfCheese:
        cheeseMap[(mazeHeight-cheese[1]-1, cheese[0])] = 1


def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    
    global heatMap
    global cheeseMap
    # We use Dijkstra's algorithm from the current location
    (routes, distances) = dijkstra(mazeMap, playerLocation)
    
    # We find the closest pieces of cheese using the distances
    closestPieceOfCheese = findClosestPieceOfCheese(distances, piecesOfCheese)
    # Using the routes, we find the next move
    resultMoves = pathToMoves(routesToPath(routes, closestPieceOfCheese))
    heatMap[(mazeHeight-playerLocation[1]-1, playerLocation[0])] += 1
    if len(resultMoves) == 0:
        return MOVE_DOWN
    else:
        return resultMoves[0]


def postprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    print("Cheeses found {}: {}".format("python",playerScore))    

    if playerScore > opponentScore:
        print("Wouhou j'ai gagné!!!")
    elif playerScore < opponentScore:
        print("Mince j'ai perdu")
    else:
        print("Match null")
    
    '''plt.subplot(2, 1, 1)
    ay = sns.heatmap(cheeseMap, cmap="binary", linewidths=.1, xticklabels=False, yticklabels=False)
    plt.plot()
    plt.subplot(2, 1, 2)
    ax = sns.heatmap(heatMap, cmap="YlGnBu", xticklabels=False, yticklabels=False)
    plt.plot()
    plt.show()'''
    