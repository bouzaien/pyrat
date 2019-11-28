TEAM_NAME = "Greedy"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

moves = []
finalRoute = []

import functions as fn
import time
import dj as dij


def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :
   global moves
   global finalRoute
   finalRoute = fn.run2opt(mazeMap,playerLocation, piecesOfCheese, 0.9*timeAllowed)


def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    global moves 
    newList = [piece for piece in finalRoute if piece in piecesOfCheese]
    t0 = time.time()
    move = dij.A_to_B(mazeMap, playerLocation, newList[0])[0]
    return move


def postprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    print("Cheeses found {}: {}".format("python",playerScore))    

    if playerScore > opponentScore:
        print("Wouhou j'ai gagné!!!")
    elif playerScore < opponentScore:
        print("Mince j'ai perdu")
    else:
        print("Match null")
