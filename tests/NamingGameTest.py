import unittest
from variants.BaselineNG import *
from namingGameTools import Strategy
from namingGameTools.MatrixFactory import *
from exports.export import *
import numpy as np

class NamingGameTest(unittest.TestCase):
  #setup the Naming Game (using actions export) for games that only
  def setUp(self):
    self.singleIterationMono = BaselineNG(maxIterations=1, simulations=1, strategy=Strategy.mono, output=["actions"], display=False)
    self.singleIterationMulti = BaselineNG(maxIterations=1, simulations=1, strategy=Strategy.multi, output=["actions"], display=False)
    self.singleItMultSim = BaselineNG(maxIterations=1, simulations=2, strategy=Strategy.multi, output=["actions"], display=False)
    self.multiIT = BaselineNG(maxIterations=2, simulations=1, strategy=Strategy.multi, output=["actions"], display=True)
    self.numberOfAgents = 5
    self.lattice = MatrixFactory().makeLatticeMatrix(self.numberOfAgents, 2)
    self.singleConnection = np.array([[0,1],[1,0]])

  def test_startEmptyMemory(self):
    """Prior to starting a new Naming Game, every agent has no previous memory of the previous game"""
    #create an output test object that checks whether we have empty memory at the start and between simulations
    outputTest = export("test", self.singleIterationMono)
    def testEveryAgent(noOfAgents):
      for i in range(noOfAgents):
        self.assertFalse(outputTest.ng.memory[i])
    outputTest.setup = testEveryAgent
    #add this output object to singleIterationMono
    self.singleIterationMono.output.append(outputTest)
    #start game with lattice
    self.singleIterationMono.start(self.lattice)
    #start game with lattice again (to test)
    self.singleIterationMono.start(self.lattice)

  def test_influenceBetweenSims(self):
    """The simulations in a single Naming Game are independent from each other"""
    assertFalse = self.assertFalse
    #create new subclass of BaselineNG to override setupSimulation
    class BNG(BaselineNG):
      def setupSimulation(self):
        #perform the usual setupSimulation
        super().setupSimulation()
        for memory in self.memory:
          #check that memory isn't transferred between simulations
          assertFalse(memory)
    multiSim = BNG(maxIterations=1, simulations=2, strategy=Strategy.multi, output=["actions"], display=False)
    multiSim.start(self.lattice)

  def test_inventAdopt(self):
    """The very first iteration of the Naming Game, every speaker will invent a name and both listeners will adopt"""
    #Since multi doensn't provide us with exact the same amount of agents every time, we are using mono for this test
    #Get output
    output = self.singleIterationMono.start(self.lattice)
    actions = output["actions"]
    #Single simulation
    action = actions[0]
    #Since our simulation is running one iteration, there should only be one invention and two adoptions
    self.assertEquals(1, action["invent"])
    self.assertEquals(2, action["adopt"])

  def test_success(self):
    """If a speaker listener pair agrees about the name of an object, the Naming Game reaches a success"""
    # Using single connection: on Iteration 1 the pair will invent a name, on Iteration 2, they will agree to it
    # Get output
    output = self.multiIT.start(self.singleConnection)
    actions = output["actions"]
    # Single simulation
    action = actions[0]
    self.assertEquals(1, action["success"])

  def test_consensus(self):
    """If the Naming Game reaches a final consensus, the simulation stops early"""
    # create an output test object that checks whether we have empty memory at the start and between simulations
    assertEq = self.assertEquals
    class test(export):
      def onIteration(self, sim, it):
        self.ng.consensus = 1

      def onConsensus(self, sim, it, consensus):
        self.ng.finalConsensus = True

      def onFinalConsensus(self, sim, it):
        #Iteration 0 is the first iteration
        assertEq(0, it)
    outputTest = test("test", self.multiIT)
    self.multiIT.output.append(outputTest)
    #If we reach consensus on every iteration, we should be able to stop the game after one iteration
    output = self.multiIT.start(self.singleConnection)
    actions = output["actions"]
    # Single simulation
    action = actions[0]
    #If the game stopped after one iteration, a successfull game is not possible
    self.assertEquals(0, action["success"])




