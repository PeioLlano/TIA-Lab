# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from cmath import inf, sqrt
from time import sleep
from turtle import screensize
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "* YOUR CODE HERE *"
        if successorGameState.isWin():
            return float(inf)
        if successorGameState.isLose():
            return float(-inf)
            
        # Calcular distancia al fantasma más cercano
        nearestGhostDistance = float(inf)
        for ghostPos in newGhostPositions:
            manhattanGhost = abs(newPos[0] - ghostPos[0]) + abs(newPos[1] - ghostPos[1])
            if manhattanGhost < nearestGhostDistance:
                nearestGhostDistance = manhattanGhost
        # Si el estado nos pone en peligro de ser comidos intentar evitarlo
        if nearestGhostDistance <= 1:
            return 0

        # Calcular distancia a la comida más cercana
        nearestFoodDistance = float(inf)
        for food in newFood.asList():
            manhattanFood = abs(newPos[0] - food[0]) + abs(newPos[1] - food[1])
            if manhattanFood < nearestFoodDistance:
                nearestFoodDistance = manhattanFood
                
        return 1 / (len(newFood.asList()) + nearestFoodDistance / 20)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #inicializar el valor v
        v = float("-inf") 
        minimaxP = float("-inf") 

        #inicializar mejor accion
        mejorAccion = None

        #obtener las acciones legales
        accionesPac = gameState.getLegalActions(0)

        #obtener los sucesores de cada accion legal 
        for accion in accionesPac:
            sucesor = gameState.generateSuccessor(0, accion)
            
            v = self.minValue(sucesor, 1, self.depth)

            if (minimaxP < v):
                minimaxP = v
                mejorAccion = accion
            
        
        return mejorAccion

    def minValue(self, gameState, ghostIndex, profundidad):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        else:
            v = float("inf")
            
            #obtener las acciones legales
            accionesGhost = gameState.getLegalActions(ghostIndex)

            #obtener los sucesores de cada accion legal 
            for accion in accionesGhost:
                sucesor = gameState.generateSuccessor(ghostIndex, accion)

                if (gameState.getNumAgents() == ghostIndex+1):
                    v = min(v, self.maxValue(sucesor, profundidad))
                else:
                    v = min(v, self.minValue(sucesor, ghostIndex+1, profundidad))
                    
            return v
            
    def maxValue(self, gameState, profundidad):

        profundidad = profundidad-1

        if gameState.isLose() or gameState.isWin() or profundidad <= 0:
            return self.evaluationFunction(gameState)
        else:
            v = float("-inf")
            
            #obtener las acciones legales
            accionesPac = gameState.getLegalActions(0)

            #obtener los sucesores de cada accion legal 
            for accion in accionesPac:
                sucesor = gameState.generateSuccessor(0, accion)

                v = max(v, self.minValue(sucesor, 1, profundidad))

            return v



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #inicializar el valor v, alfa y beta
        v = float("-inf")  
        minimaxP = float("-inf")    
        alfa = float("-inf") 
        beta = float("inf") 

        #inicializar mejor accion
        mejorAccion = None

        #obtener las acciones legales
        accionesPac = gameState.getLegalActions(0)

        #obtener los sucesores de cada accion legal 
        for accion in accionesPac:
            sucesor = gameState.generateSuccessor(0, accion)
            
            v = self.minValueAB(sucesor, 1, self.depth, alfa, beta)

            if (minimaxP < v):
                minimaxP = v
                mejorAccion = accion

            alfa = max(alfa, v)
            
        
        return mejorAccion

    def minValueAB(self, gameState, ghostIndex, profundidad, alfa, beta):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        else:
            v = float("inf")
            
            #obtener las acciones legales
            accionesGhost = gameState.getLegalActions(ghostIndex)

            #obtener los sucesores de cada accion legal 
            for accion in accionesGhost:
                sucesor = gameState.generateSuccessor(ghostIndex, accion)

                if (gameState.getNumAgents() == ghostIndex+1):
                    v = min(v, self.maxValueAB(sucesor, profundidad, alfa, beta))
                else:
                    v = min(v, self.minValueAB(sucesor, ghostIndex+1, profundidad, alfa, beta))
                
                if (v < alfa):
                    return v

                beta = min(beta, v)

            return v
            
    def maxValueAB(self, gameState, profundidad, alfa, beta):

        profundidad = profundidad-1

        if gameState.isLose() or gameState.isWin() or profundidad <= 0:
            return self.evaluationFunction(gameState)
        else:
            v = float("-inf")
            
            #obtener las acciones legales
            accionesPac = gameState.getLegalActions(0)

            #obtener los sucesores de cada accion legal 
            for accion in accionesPac:
                sucesor = gameState.generateSuccessor(0, accion)

                v = max(v, self.minValueAB(sucesor, 1, profundidad, alfa, beta))
            
                if (v > beta):
                    return v

                alfa = max(alfa, v)

            return v



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #inicializar el valor v
        v = float("-inf") 
        minimaxP = float("-inf")  

        #inicializar mejor accion
        mejorAccion = None

        #obtener las acciones legales
        accionesPac = gameState.getLegalActions(0)

        #obtener los sucesores de cada accion legal 
        for accion in accionesPac:
            sucesor = gameState.generateSuccessor(0, accion)

            v = self.expectimax(sucesor, self.depth, 1)

            if (minimaxP < v):
                minimaxP = v
                mejorAccion = accion

        return mejorAccion

    def maxValueEx(self, gameState, profundidad):

        profundidad = profundidad-1

        if gameState.isLose() or gameState.isWin() or profundidad <= 0:
            return self.evaluationFunction(gameState)
        else:
            v = float("-inf")
            
            #obtener las acciones legales
            accionesPac = gameState.getLegalActions(0)

            #obtener los sucesores de cada accion legal 
            sucesores = {}    
            for accion in accionesPac:
                sucesor = gameState.generateSuccessor(0, accion)

                v = max(v, self.expectimax(sucesor, profundidad, 1))

            return v

    def expectimax(self, gameState, profundidad, ghostIndex):

        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        else:
            v = 0
            
            #obtener las acciones legales
            accionesGhost = gameState.getLegalActions(ghostIndex)

            #Calcular probabilidad
            probabilidad = 1 / len(accionesGhost)

            #obtener los sucesores de cada accion legal 
            for accion in accionesGhost:
                sucesor = gameState.generateSuccessor(ghostIndex, accion)

                if (gameState.getNumAgents() == ghostIndex+1):
                    v += self.maxValueEx(sucesor, profundidad)
                else:
                    v += self.expectimax(sucesor,profundidad, ghostIndex+1)

            return (v*probabilidad)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    foodCount = currentGameState.getNumFood()
    score = currentGameState.getScore()
    ghostPositions = currentGameState.getGhostPositions()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    scaredTime = ghostStates[0].scaredTimer

    if currentGameState.isWin():
        return float(inf)
    if currentGameState.isLose():
        return float(-inf)

    # Calcular la distancia al fantasma más cercano
    nearestGhostDistance = float(inf)
    for ghostPos in ghostPositions:
        manhattanGhost = abs(pacmanPos[0] - ghostPos[0]) + abs(pacmanPos[1] - ghostPos[1])
        if manhattanGhost < nearestGhostDistance:
            nearestGhostDistance = manhattanGhost
    
    # Si hay fantasmas asustados, intentar que pacman se coma al fantasma más cercano
    if scaredTime > 0:
        return 2000/nearestGhostDistance + 10*score

    # Calcular la distancia a la comida más cercana
    nearestFoodDistance = float(inf)
    for food in foodList:
        manhattanFood = abs(pacmanPos[0] - food[0]) + abs(pacmanPos[1] - food[1])
        if manhattanFood < nearestFoodDistance:
            nearestFoodDistance = manhattanFood

    # Calcular la distancia a la cápsula más cercana
    nearestCapsuleDistance = float(inf)
    for capsule in capsules:
        manhattanCapsule = abs(pacmanPos[0] - capsule[0]) + abs(pacmanPos[1] - capsule[1])
        if manhattanCapsule < nearestCapsuleDistance:
            nearestCapsuleDistance = manhattanCapsule

    return score + 4/foodCount + 2/nearestFoodDistance + nearestGhostDistance/4 + 5/nearestCapsuleDistance


# Abbreviation
better = betterEvaluationFunction
