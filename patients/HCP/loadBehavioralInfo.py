#Imports for processing csv_results files and dataframes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Access the behavioral csv_results file in patients folder
behavioral = pd.read_csv("behavioral.csv")

#Subjects are a txt file seperated by newlines so we need to process the txt and add the subjects to a list
subjectsStream = open("subjects.txt", "r")
subjects = subjectsStream.read().split("\n")

#Remove the last element of the list because it is an empty string
subjects.pop()

#Subjects are strings to convert them to integers
subjects = [int(subject) for subject in subjects]

#Filter the behavioral datatframe to only contain the subjects in the subjects list
behavioral = behavioral[behavioral["Subject"].isin(subjects)]

print(behavioral)

#Export behavioral information to csv_results/ouput/behavioralInformation.csv_results
behavioral.to_csv("behavioralInformation.csv", index=False)
