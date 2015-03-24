# multiAgents.py
# --------------

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin():
            return float("inf")

        score = successorGameState.getScore()
        nbAgents = currentGameState.getNumAgents()
        
        closestGhost = 100
        for i in xrange(1, nbAgents):
            closestGhost = min(closestGhost, util.manhattanDistance(successorGameState.getGhostPosition(i), newPos))
        score += max(closestGhost, 2)

        closestFood = 100
        for food in newFood.asList():
            closestFood = min(closestFood, util.manhattanDistance(food, newPos))
        score -= 4*closestFood

        if newPos in successorGameState.getCapsules():
            score += 150

        if currentGameState.getNumFood() > successorGameState.getNumFood():
            score += 200

        if action == Directions.STOP:
            score -= 5

        #print score
        return score

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
    def maxValue(self, gameState, depth):
        if(gameState.isWin() or gameState.isLose() or depth==0):
            return self.evaluationFunction(gameState)

        #Pacman
        bestValue=float("-inf")
        for action in gameState.getLegalActions(0):
            v = self.minValue(gameState.generateSuccessor(0, action), depth, 1)
            bestValue =	max(v, bestValue)

        return bestValue

    def minValue(self, gameState, depth, index):
        if(gameState.isWin() or gameState.isLose() or depth==0):
            return self.evaluationFunction(gameState)

        #Ghost
        bestValue=float("inf")
        for action in gameState.getLegalActions(index):
            if(index==(gameState.getNumAgents()-1)):
                v = self.maxValue(gameState.generateSuccessor(index, action), depth-1)
            else:
                v = self.minValue(gameState.generateSuccessor(index, action), depth, index+1)
            bestValue =	min(v, bestValue)
    
        return bestValue

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
        """

        nextAction = Directions.STOP
        value = float("-inf")

        for action in gameState.getLegalActions():
            nextState = gameState.generateSuccessor(0, action)
            previousValue = value
            value = max(value, self.minValue(nextState, self.depth, 1))

            if value > previousValue:
                nextAction=action

        #print value
        return nextAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxValue(self, gameState, depth, alpha, beta):
        if(gameState.isWin() or gameState.isLose() or depth==0):
            return self.evaluationFunction(gameState)

        #Pacman
        bestValue=float("-inf")
        for action in gameState.getLegalActions(0):
            v = self.minValue(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
            bestValue =	max(v, bestValue)
    
            if bestValue > beta:
                return bestValue
            alpha=max(alpha, bestValue)

        return bestValue

    def minValue(self, gameState, depth, index, alpha, beta):
        if(gameState.isWin() or gameState.isLose() or depth==0):
            return self.evaluationFunction(gameState)

        #Ghost
        bestValue=float("inf")
        for action in gameState.getLegalActions(index):
            if(index==(gameState.getNumAgents()-1)):
                v = self.maxValue(gameState.generateSuccessor(index, action), depth-1, alpha, beta)
            else:
                v = self.minValue(gameState.generateSuccessor(index, action), depth, index+1, alpha, beta)
            bestValue =	min(v, bestValue)
    
            if bestValue < alpha:
                return bestValue
            beta=min(beta, bestValue)

        return bestValue

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        nextAction = Directions.STOP
        value = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for action in gameState.getLegalActions():
            nextState = gameState.generateSuccessor(0, action)
            previousValue = value
            value = max(value, self.minValue(nextState, self.depth, 1, alpha, beta))

            if value > previousValue:
                nextAction=action

            if value > beta:
                return nextAction

            alpha = max(alpha, value)

        #print value
        return nextAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxValue(self, gameState, depth):
        if(gameState.isWin() or gameState.isLose() or depth==0):
            return self.evaluationFunction(gameState)

        #Pacman
        bestValue=float("-inf")
        for action in gameState.getLegalActions(0):
            v = self.expValue(gameState.generateSuccessor(0, action), depth, 1)
            bestValue =	max(v, bestValue)

        return bestValue

    def expValue(self, gameState, depth, index):
        if(gameState.isWin() or gameState.isLose() or depth==0):
            return self.evaluationFunction(gameState)

        #Ghost
        v=0.0
        nb=0.0
        for action in gameState.getLegalActions(index):
            if(index==(gameState.getNumAgents()-1)):
                v += self.maxValue(gameState.generateSuccessor(index, action), depth-1)
            else:
                v += self.expValue(gameState.generateSuccessor(index, action), depth, index+1)
            nb += 1
    
        v=v/nb
        return v

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        nextAction = Directions.STOP
        value = float("-inf")

        for action in gameState.getLegalActions():
            nextState = gameState.generateSuccessor(0, action)
            previousValue = value
            value = max(value, self.expValue(nextState, self.depth, 1))

            if value > previousValue:
                nextAction=action

        #print value
        return nextAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      For this evaluation function, I used the same implementation as in question 1, but instead of adding random values to make up a score,
      I decided to use weighted reciprocals of important values, such as: closestGhost, closestFood, closestCapsule.
      I also felt I should add two values to the score that I thought are important: the sum of newScaredTimes, and the weight reciprocal
      of the number of food left to eat.
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    if currentGameState.isWin():
        return float("inf")

    if currentGameState.isLose():
        return float("-inf")

    score = currentGameState.getScore()

    for time in newScaredTimes:
        score += time

    nbAgents = currentGameState.getNumAgents()
    
    closestGhost = 100
    for i in xrange(1, nbAgents):
        closestGhost = min(closestGhost, util.manhattanDistance(currentGameState.getGhostPosition(i), newPos))

    closestFood = 100
    for food in newFood.asList():
        closestFood = min(closestFood, util.manhattanDistance(food, newPos))

    closestCapsule = 100
    for capsule in currentGameState.getCapsules():
        closestCapsule = min(closestCapsule, util.manhattanDistance(capsule, newPos))

    if closestGhost:
        score += 15.0/closestGhost

    if closestFood:
        score += 10.0/closestFood

    if closestCapsule:
        score += 8.0/closestCapsule

    nbFood = len(newFood.asList())
    if nbFood:
        score += 20.0/nbFood
    
    return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

