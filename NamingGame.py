from abc import ABC, abstractmethod
import AgentPairs as ap
import numpy as np

#Here, we will be defining the abstract superclass for all of the strategies for the Naming game, in general all the Naming Game variants use the same skeleton

#TODO make methods private
class NamingGame(ABC):

  def __init__(self, simulations=2, iterations=50, display=False):
    self.simulations = simulations
    self.iterations = iterations
    self.display = display

  #setup the game
  def setup(self, matrixNetwork):
    #get number of agents
    numberOfAgents = len(matrixNetwork)
    #create a list filled with no. agents worth of empty lists, these will be the memory of the agents
    self.memory = [ [] for _ in range(numberOfAgents) ]
    #generate the context
    self.context = self.generateContext()
    #keep track of the amount of names generated
    self.inventedNames = 0

  #Generates the context for The Naming Game
  @abstractmethod
  def generateContext(self):
    pass

  #Name for object and topic are interchangeable, my usage is to align as closely to the Naming Game documentation
  #Looks up an object from memory (can return zero, one or multiple names)
  @abstractmethod
  def produce(self, object, agent):
    pass

  #Looks up a name from memory (can either return one object or no object)
  #Listener method
  @abstractmethod
  def interpret(self, name, agent):
    pass

  #Creates a new name for a certain topic
  #Speaker Method
  @abstractmethod
  def invent(self, topic, agent):
    #increase name count
    self.inventedNames += 1

  #Adopts a certain name for a topic
  #Speaker Method
  @abstractmethod
  def adopt(self, name, topic, agent):
    pass

  #Chooses an object from the context (called the topic)
  @abstractmethod
  def pick(self, agent, context):
    pass

  #Code that runs in case of a success
  @abstractmethod
  def success(self, speaker, listener, topic, name):
    if self.display:
      print("Agent " + str(speaker) + " and Agent " + str(listener) + " agreed that object " + str(
        topic) + " has the name " + str(name))

  #Code that runs in case of a failure
  @abstractmethod
  def failure(self, speaker, listener, intendedTopic, perceivedTopic, name):
    if self.display:
      print("Agent " + str(speaker) + " and Agent " + str(listener) + " did not agree with the name " + str(
        name) + ". Intended Topic: " + str(intendedTopic) + ", Perceived Topic: " + str(perceivedTopic))

  #Does one iteration of the Naming Game for all pairs
  def run(self, matrixNetwork):
    agentPairs = ap.AgentPairs().generate(matrixNetwork)
    for speaker, listener in agentPairs:
      #speaker picks a topic from context
      intendedTopic = self.pick(speaker, self.context)
      #speaker produces a name for said topic
      name = self.produce(intendedTopic, speaker)
      #listeners interprets name and gives his own topic
      perceivedTopic = self.interpret(name, listener)
      #if we found a topic
      if perceivedTopic:
        if intendedTopic == perceivedTopic:
          self.success(speaker, listener, intendedTopic, name)
        else: self.failure(speaker, listener, intendedTopic, perceivedTopic, name)
      #if we haven't found a topic, listener should adopt it
      else: self.adopt(name, intendedTopic, listener)

  #Starts the Naming Game with the desired amount of simulations
  def start(self, matrixNetwork):
    print("Starting the Naming Game")
    #create a table
    nameTable = np.zeros((self.iterations, self.simulations))
    for sim in range(self.simulations):
      self.setup(matrixNetwork)
      for iteration in range(self.iterations):
        print("Iteration " + str(iteration))
        self.run(matrixNetwork)
        #update name table
        nameTable[iteration, sim] = self.inventedNames
      #visualize the simulation
      # display the current state and print vocabulary
      if self.display:
        print("Simulation " + str(sim))
        for i in range(len(self.memory)):
          print("Agent " + str(i))
          print(self.memory[i])
    #return median
    return np.mean(nameTable, axis=1)






