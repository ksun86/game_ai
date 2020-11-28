# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qvals = util.Counter()
        return

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        qvalue = self.qvals[(state,action)]
        return qvalue

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        qvals = []
        for action in actions:
            q = self.getQValue(state, action)
            qvals.append(q)
        # endfor
        return 0.0 if not len(qvals) else max(qvals)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        lActions = self.getLegalActions(state)
        if not len(lActions):
            return None
        qval = -10000000000
        for laction in lActions:
            tempval = self.getQValue(state, laction)
            if tempval > qval:
                qval = tempval
                action = laction
            # endif
        # endfor
        return action


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if not len(legalActions): return action
        randomchance = util.flipCoin(self.epsilon)
        action = random.choice(legalActions) if randomchance else self.getPolicy(state)
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        curval = self.getQValue(state, action)
        newval = (1-self.alpha) * curval \
            + self.alpha * (reward + self.discount * self.getValue(nextState) )
        self.qvals[(state, action)] = newval
        return

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        #self.weights = util.Counter()
        fname1 = ('weights')
        f1 = file(fname1, 'r')
        print("init")
        try: 
            recorded1 = cPickle.load(f1)
            print "-----++++++++++----"
            print recorded1
            self.weights = recorded1
        
        except:
            print("exception")
            self.weights = util.Counter()
        
        finally: 
            f1.close()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        qval = 0.0 
        feats = self.featExtractor.getFeatures(state, action)
        for f in feats:
            qval += feats[f] * self.weights[f]
        # endfor
        return qval

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        feats = self.featExtractor.getFeatures(state, action)
        diff = reward + self.discount * self.getValue(nextState) \
                - self.getQValue(state, action)
        for f in feats:
            self.weights[f] += self.alpha * diff * feats[f]
        # endfor
        return

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print('Weights at the end of the game play')
            print(self.weights)
            pass

class GTApproximateQAgent(ApproximateQAgent):
    """
       GTApproximateQLearningAgent
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        try: 
            fname1 = ('gtweights')
            f1 = file(fname1, 'r')
            print("init")
            recorded1 = cPickle.load(f1)
            print "-----++++++++++----"
            print recorded1
            self.weights = recorded1
            f1.close()
        except:
            print("exception")
            self.weights = util.Counter()
            

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        feats = self.featExtractor.getFeatures(state, action)
        qval = sum(feats[f] * self.weights[f] for f in feats)
        return qval

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        feats = self.featExtractor.getFeatures(state, action)
        diff = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)
        for f in feats:
            self.weights[f] += self.alpha * diff * feats[f]
        return

    def final(self, state):
        PacmanQAgent.final(self, state)
        if self.episodesSoFar == self.numTraining:
            print('Weights at the end of the game play')
            print(self.weights)
            pass
