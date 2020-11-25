# PacMan-RL
PacMan Reinforcement Learning project from UC Berkley Intro to AI 

# Steps to run the project

## Using Q-learning Agent
1. python pacman.py -p PacmanQAgent -x 1800 -n 2000 -l smallGrid

This command will run the pacman.py file with simple Q-learning Agent.
1800 game play will be used to train the agent.
remaining 200 game will be for testing the agent.
To change the grid type use -l option.

Simple Q-learning Agent only works for smallgrid. For larger grids, it will require very large number of training iterations. So for larger grids we wil use approximate Q-learning. 

## Using Approximate Q-learning Agent

1. python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 40 -n 55 -l mediumGrid 

2. python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 55 -l mediumClassic

3. python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 100 -n 110 -l trickyClassic

Above commands can be used to run pacman.py with approximate Q-learning agent. 
-x option is used to specify number of training episodes
-n option is used to specify number of total episodes
-l option can be used to change the type of grid

## Available Grids
- capsuleClassic
- contestClassic
- mediumClassic
- mediumGrid
- minimaxClassic
- openClassic
- originalClassic
- smallClassic
- smallGrid
- testClassic
- trappedClassic
- trickyClassic
