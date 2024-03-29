from matplotlib import pyplot as plt
from patients.patientData import *
from patients.patientData import brumeg_functional_convergence

patientData = brumeg_functional_convergence

#get the unique values of the Subject row
patientNames = patientData['Subject'].unique().tolist()

# groupSize = len(patientNames) // 50
groupSize = 4

patientGroups = [patientNames[i:i+groupSize] for i in range(0, len(patientNames), groupSize)]

colors = ['blue', 'red', 'cyan', 'magenta', 'green', 'purple']

consensusScoreList = [0.8, 0.9,0.95, 1]

#help procedures for the boxplot
# function for setting the colors of the box plots pairs
def setBoxColors(bp):
  for index, box in enumerate(bp['boxes']):
    plt.setp(box, color=colors[index])

def consensusTime():
  for i, patientGroup in enumerate(patientGroups):
    #set titles of the graph
    plt.title(f"Consensus Time (ABNG, 100 sim, using patient SC group {i})")
    plt.ylabel("Amount of Games played")
    plt.xlabel("Patient Number")
    #draw legend (draws lines, uses these lines for the legend and then undraws them)
    #draw lines
    lines = [plt.plot([1, 1], color=color)[0] for color in colors]
    #create labels for the lines
    consensusScoreStringList = [f"Convergence Rate : {rate}" for rate in consensusScoreList]
    #draw legend
    plt.legend(lines, consensusScoreStringList)
    #hide lines we've drawn
    list(map(lambda handle: handle.set_visible(False), lines))

    #generate positions for all boxplots of a patient group
    positions = [[n for n in range(i, i + len(consensusScoreList))] for i in
                 range(0, len(patientGroup) * len(consensusScoreList), len(consensusScoreList))]

    #get median of positions as position for the ticks
    ticks = [np.mean(lst) for lst in positions]

    consensusMatrix = []
    #per patient get consensus Iteration of every consensusscore
    for patient in patientGroup:
      consensusList = []
      for consensusScore in consensusScoreList:
        #get array of values where this patient reached consensus
        consensus = getConsensusIterationOfSubject(patientData, patient, consensusScore)
        consensusList.append(consensus)
      #add filled in consensusList to matrix
      consensusMatrix.append(consensusList)

    for index, row in enumerate(consensusMatrix):
      bp = plt.boxplot(row, positions=positions[index], widths=0.6)
      setBoxColors(bp)

    #set ticks
    plt.xticks(ticks, patientGroup)

    #show graph
    plt.show()

consensusTime()


