import unittest
import MatrixFactory as mf
import numpy as np

class MatrixFactoryTest(unittest.TestCase):
  #setup the test
  def setUp(self):
    #create a new triangular and regular matrix factory
    self.rFactory = mf.MatrixFactory(triangular=False)
    self.tFactory = mf.MatrixFactory(triangular=True)

  def test_asymCreation(self):
    """A matrix factory should be able to produce all implemented matrices"""
    lattice = self.rFactory.makeLatticeMatrix(20, 4)
    scaleFree = self.rFactory.makeScaleFreeMatrix(10)
    smallWorld = self.rFactory.makeSmallWorldMatrix(15, 5, 4)

  def test_symCreation(self):
    """A matrix factory should be able to produce a lower triangular matrix version of every matrix"""
    lattice = self.tFactory.makeLatticeMatrix(20, 4)
    scaleFree = self.tFactory.makeScaleFreeMatrix(10)
    smallWorld = self.tFactory.makeSmallWorldMatrix(15, 5, 4)
    self.assertTrue(np.allclose(lattice, np.tril(lattice)))  # check if lower triangular
    self.assertTrue(np.allclose(scaleFree, np.tril(scaleFree)))  # check if lower triangular
    self.assertTrue(np.allclose(smallWorld, np.tril(smallWorld)))  # check if lower triangular

  def test_equalityCreation(self):
    """A lattice matrix created from a symmetrical allowance should be the same as the lower triangular of a matrix created without this allowance"""
    #Full matrix
    l1 = self.rFactory.makeLatticeMatrix(20, 4)
    #Lower triangular matrix
    l2 = self.tFactory.makeLatticeMatrix(20, 4)
    self.assertTrue(np.allclose(l2, np.tril(l1)))  # check if same

  def test_latticeConnections(self):
    """Each agent in a lattice is connected exactly to a certain amount of neighbors"""
    def doTest(pair):
      print("Testing Pair: " + str(pair))
      agents = pair[0]
      neighbours = pair[1]
      asymLattice = self.rFactory.makeLatticeMatrix(agents, neighbours)
      symLattice = self.tFactory.makeLatticeMatrix(agents, neighbours)
      #enforce neighbours to be even (round all odd numbers down)
      neighbours = (neighbours // 2) * 2
      nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(asymLattice)
      nonZeroCount = len(nonZeroRowNrs)
      # An asymmetrical lattice matrix has 20 agent *4 neighbors= 80 connections
      self.assertEqual(agents*neighbours, nonZeroCount, "Asymmetrical Error")
      nonZeroRowNrsSym, nonZeroColumnNrsSym = np.nonzero(symLattice)
      nonZeroCountSym = len(nonZeroRowNrsSym)
      # The symmetrical lattice should be equal to half the asymmetrical connections (in this case 40)
      self.assertEqual(agents*neighbours / 2, nonZeroCountSym, "Symmetrical Error")
      ##ASK ABOUT UNEVEN NEIGHBOURS
    latticePairs = [(20,4), (30,6), (99, 4), (15,10), (24, 5)]
    # counter-examples = (15,5)

    for pair in latticePairs:
      doTest(pair)

  def test_scaleFreeConnections(self):
    """Each agent in a scale free matrix is connected depending on the establishing links"""

    def doTest(pair):
      print("Testing Pair: " + str(pair))
      agents = pair[0]
      establishedLinks = pair[1]
      asymScaleFree= self.rFactory.makeScaleFreeMatrix(agents, establishedLinks)
      symScaleFree = self.tFactory.makeScaleFreeMatrix(agents, establishedLinks)
      nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(asymScaleFree)
      nonZeroCount = len(nonZeroRowNrs)
      #expected non zero elements = 8 (starting connections from 4 agents) + 2 (two-way connection) * Established Links * remaining agents (agents - 4)
      self.assertEqual(8 + 2 * establishedLinks * (agents - 4), nonZeroCount, "Asymmetrical Error")
      nonZeroRowNrsSym, nonZeroColumnNrsSym = np.nonzero(symScaleFree)
      nonZeroCountSym = len(nonZeroRowNrsSym)
      # The symmetrical lattice should be equal to half the asymmetrical connections
      self.assertEqual(4 + establishedLinks * (agents - 4), nonZeroCountSym, "Symmetrical Error" + str(symScaleFree))

    #we are limited to max 3 establishing links
    scaleFreePairs = [(16, 0), (10, 1), (20, 2), (37, 3), (14, 3), (400, 3)]
    #Counter Example: any establishing links higher than 3


    for pair in scaleFreePairs:
      doTest(pair)

  def test_smallWorldMatrix(self):
    """Each agent in a scale free matrix is connected dependings on fixed neighbours + random links"""
    def doTest(set):
      print("Testing Set: " + str(set))
      agents = set[0]
      neighbours = set[1]
      random = set[2]
      asymSmallWorld = self.rFactory.makeSmallWorldMatrix(agents, neighbours, random)
      symSmallWorld = self.tFactory.makeSmallWorldMatrix(agents, neighbours, random)
      # enforce neighbours to be even (round all odd numbers down)
      neighbours = (neighbours // 2) * 2
      nonZeroRowNrs, nonZeroColumnNrs = np.nonzero(asymSmallWorld)
      nonZeroCount = len(nonZeroRowNrs)
      # An asymmetrical lattice matrix has 20 agent *4 neighbors= 80 connections + 2 * random links
      self.assertEqual(agents*neighbours + 2 * random, nonZeroCount, "Asymmetrical Failure")
      nonZeroRowNrsSym, nonZeroColumnNrsSym = np.nonzero(symSmallWorld)
      nonZeroCountSym = len(nonZeroRowNrsSym)
      self.assertEqual(agents*neighbours/2 + random, nonZeroCountSym, "Symmetrical Failure")

    ##ASK ABOUT UNEVEN NEIGHBOURS
    smallWorldSets = [(20,4, 5), (30,6, 8), (99, 4, 3), (15,10,5), (24, 5, 6)]

    for set in smallWorldSets:
      doTest(set)


if __name__ == '__main__':
  unittest.main()

