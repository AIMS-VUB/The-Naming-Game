from abc import ABC, abstractmethod
from namingGameTools import AgentPairs as ap, Strategy
from exports.possibleExports import possibleExports


#Here, we will be defining the abstract superclass for all of the strategies for the Naming game, in general all the Naming Game variants use the same skeleton

#TODO make methods private
class NamingGame(ABC):

  def __init__(self, simulations=2, maxIterations=50, display=False, strategy=Strategy.multi, output=[], consensusScore = [1]):
    self.simulations = simulations
    self.maxIterations = maxIterations
    self.displayEnabled = display
    self.strategy = strategy
    #create a list with all export objects
    self.output = list(map(lambda name: possibleExports[name](name, self), output))
    #get class name
    self.name = self.__class__.__name__
    self.consensusScore = consensusScore
    #sort consensusScore list to ensure the biggest consensus score becomes last
    self.consensusScore.sort()

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
  @abstractmethod
  def interpret(self, name, agent):
    pass

  #Creates a new name for a certain topic
  @abstractmethod
  def invent(self, topic, agent):
    #perform the everyInvent action for every export object
    list(map(lambda export: export.onInvent(), self.output))

  #Adopts a certain name for a topic
  @abstractmethod
  def adopt(self, name, topic, listener, speaker):
    list(map(lambda export: export.onAdopt(name, listener), self.output))
    # say that the agent has adopted this new method
    self.display(f"Agent {listener} has adopted the name {name} for topic {topic} from agent {speaker}")

  @abstractmethod
  def remove(self, name, topic, agent):
    list(map(lambda export: export.onRemove(name, agent), self.output))
    self.display(f"Removed this pair from Agent memory {agent}: {name}, {topic}")

  #Chooses an object from the context (called the topic)
  @abstractmethod
  def pick(self, agent, context):
    list(map(lambda export: export.onPick(agent, context), self.output))

  #Code that runs in case of a success
  @abstractmethod
  def success(self, speaker, listener, topic, name):
    list(map(lambda export: export.onSuccess(speaker, listener, topic, name), self.output))
    self.display(f"Agent {speaker} and Agent {listener} agreed that object {topic} has the name {name}")

  #Code that runs in case of a failure
  @abstractmethod
  def failure(self, speaker, listener, intendedTopic, perceivedTopic, name):
    list(map(lambda export: export.onFailure(speaker, listener, intendedTopic, perceivedTopic, name), self.output))
    self.display(f"Agent {speaker} and Agent {listener} did not agree with the name {name}. " +
                 f"Intended Topic: {intendedTopic}, Perceived Topic: {perceivedTopic}")

  #Create our own display which only prints when self.display is enabled
  def display(self, args):
    if self.displayEnabled:
      print(args)

  #setup the entire naming game
  def setup(self, numberOfAgents):
    # create a list filled with no. agents worth of empty lists, these will be the memory of the agents
    self.memory = [[] for _ in range(numberOfAgents)]
    # generate the context
    self.context = self.generateContext()

  #setup every simulation
  def setupSimulation(self):
    #clear memory
    for index in range(len(self.memory)):
      self.memory[index] = []
    #set consensus to False
    self.consensus = False
    #set final consensus to False
    self.finalConsensus = False

  #play the naming game with a speaker and listener
  def play(self, speaker, listener):
    # speaker picks a topic from context
    intendedTopic = self.pick(speaker, self.context)
    # speaker produces a name for said topic
    name = self.produce(intendedTopic, speaker)
    # listeners interprets name and gives his own topic
    perceivedTopic = self.interpret(name, listener)
    # if we found a topic
    if perceivedTopic:
      if intendedTopic == perceivedTopic:
        self.success(speaker, listener, intendedTopic, name)
      else:
        self.failure(speaker, listener, intendedTopic, perceivedTopic, name)
    # if we haven't found a topic, listener should adopt it
    else:
      self.adopt(name, intendedTopic, listener, speaker)


  #Does one iteration of the Naming Game for all pairs
  def run(self, matrixNetwork):
    #get all possible agent pairs
    agentPairs = ap.AgentPairs().generateWeighted(matrixNetwork)
    #choose pairs based of strategy
    chosenPairs = self.strategy(agentPairs)
    for speaker, listener in chosenPairs:
      self.play(speaker, listener)

  #Starts the Naming Game with the desired amount of simulations
  def start(self, matrixNetwork):
    print("Starting the Naming Game")
    print("Parameters: ")
    print("Simulations: " + str(self.simulations))
    print("Maximum Iterations: " + str(self.maxIterations))
    print("Memory Length: " + str(len(matrixNetwork)))
    if self.displayEnabled:
      print("Display Enabled")
    else: print("Display Disabled")
    numberOfAgents = len(matrixNetwork)
    self.setup(numberOfAgents)
    #notify exports that the simulations are starting
    list(map(lambda export: export.setup(numberOfAgents), self.output))
    for sim in range(self.simulations):
      print("Simulation " + str(sim))
      self.setupSimulation()
      for iteration in range(self.maxIterations):
        self.display("Iteration " + str(iteration))
        self.run(matrixNetwork)
        #update outputs on every iteration
        list(map(lambda export: export.onIteration(sim, iteration), self.output))
        #if we have reached consensus on this iteration
        if self.consensus:
          #Display that the simulation has reached a consensus
          self.display(f"Simulation {sim} has reached a consensus on iteration {iteration} with consensus score {self.consensus}")
          #notify outputs that we have reached consensus
          list(map(lambda export: export.onConsensus(sim, iteration, self.consensus), self.output))
          #if we have reached the final consensus
          if self.finalConsensus:
            #notify outputs
            list(map(lambda export: export.onFinalConsensus(sim, iteration), self.output))
            #stop the running loop
            break
          #else set consensus back to false
          else:
            self.consensus = False
      #visualize the simulation
      #update outputs
      list(map(lambda export: export.onSimulation(sim), self.output))
      self.display("Agent Memory:")
      for i in range(len(self.memory)):
        self.display(f"Agent {i}: {self.memory[i]}")
    result = {}
    # after finishing the simulations, get the output from the export objects
    for export in self.output:
      result[export.name] = export.output()
    return result







