#procedure for turning patient code from csv into readable data
import numpy as np
import pandas as pd

import os

here = os.path.dirname(os.path.abspath(__file__))

def readPatientData(name, type='connectivity'):
  #create file path
  path = here + f'/patients/{type}/{name}.csv'
  #get data from csv
  array = np.loadtxt(path, delimiter=',', dtype=float)
  # numberOfAgents is the square root of the total array length
  numberOfAgents = np.sqrt(len(array)).astype(int)
  #turn data into the right array dimension
  matrix = np.reshape(array, (numberOfAgents, numberOfAgents))
  #fill matrix diagonal with 0s
  np.fill_diagonal(matrix, 0)
  #make matrix triangular and return
  return np.tril(matrix)

# def readPatientData(name, type='connectivity'):
#   #get data from csv
#   array = np.loadtxt(f'../patients/{type}/{name}.csv', delimiter=',', dtype=float)
#   # numberOfAgents is the square root of the total array length
#   numberOfAgents = np.sqrt(len(array)).astype(int)
#   #threshold
#   def binary(el):
#     if el >= 1:
#       return 1
#     else: return 0
#   #change values into either 0 or 1 (could be removed later)
#   binaryArray = list(map(binary, array))
#   #turn data into the right array dimension
#   matrix = np.reshape(binaryArray, (numberOfAgents, numberOfAgents))
#   #make the matrix triangular
#   trig = np.tril(matrix)
#   #fill the main diagonal with 0s
#   np.fill_diagonal(trig, 0)
#   return trig

names = np.loadtxt(here + '/patients/names.csv', dtype=int)
# #
SDMT = pd.read_csv(here + '/patients/SDMT.csv')

info = pd.read_csv(here + '/patients/info.csv')

info = info.loc[info["PatientNo"].isin(names)]

#get the patients that have MS and are in the names group
MS = info.loc[info["MS"] == 1]

MS_patients = MS["PatientNo"].tolist()

control = info.loc[info["MS"] == 0]

C_patients = control["PatientNo"].tolist()