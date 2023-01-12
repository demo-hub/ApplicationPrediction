import csv
import random

import numpy as np
import pandas as pd

# Generating random data
fields = ['CompanySize', 'Experience', 'DiffYearsOfExperience',
          'ExperienceInBusinessArea', 'ExperienceWithTechnologies', 'Degree', 'PassedFirstPhase']
size = ['Small', 'Medium', 'Large']
experience = ['0-2', '2-5', '5-10', '10+']
diffYearsOfExperience = [-2, -1, 0, 1, 2]
experienceInBusinessArea = ['Yes', 'No']
experienceWithTechnologies = ['All', 'Partial', 'None']
degree = ['B.Tech', 'M.Tech', 'PhD', 'None']
passedFirstPhase = ['Yes', 'No']


filename = 'data.csv'
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(0, 1000):
        row = [random.choice(size), random.choice(experience), random.choice(
            diffYearsOfExperience), random.choice(experienceInBusinessArea), random.choice(experienceWithTechnologies), random.choice(degree), random.choice(passedFirstPhase)]
        csvwriter.writerow(row)

# Reading the data from CSV file
data = pd.read_csv('data.csv')
concepts = np.array(data.iloc[:, :-1])
print("\nInstances are:\n", concepts)
target = np.array(data.iloc[:, -1])
print("\nTarget Values are: ", target)


def train(concepts, target):

    # Initializing general and specific hypothesis
    specific_h = concepts[0].copy()
    print("\nInitialization of specific hypothesis and general hypothesis")
    print("\nSpecific Boundary: ", specific_h)
    general_h = [["?" for i in range(len(specific_h))]
                 for i in range(len(specific_h))]
    print("\nGeneric Boundary: ", general_h)

    for i, val in enumerate(concepts):
        print("\nInstance", i+1, "is ", val)
        # positive example
        if target[i] == "yes":
            for x in range(len(specific_h)):
                if val[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'
        # negative example
        if target[i] == "no":
            for x in range(len(specific_h)):
                if val[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'

        print("Specific Bundary after ", i+1, "Instance is ", specific_h)
        print("Generic Boundary after ", i+1, "Instance is ", general_h)
        print("\n")

    indices = [i for i, val in enumerate(general_h) if val == [
        '?', '?', '?', '?', '?', '?']]

    for i in indices:
        general_h.remove(['?', '?', '?', '?', '?', '?'])

    return specific_h, general_h


def predict(h, val):
    for x in range(len(h)):
        if h[x] != val[x] and h[x] != '?':
            return False
    return True


s_final, g_final = train(concepts, target)
# displaying Specific_hypothesis
print("Final Specific_h: ", s_final, sep="\n")
# displaying Generalized_Hypothesis
print("Final General_h: ", g_final, sep="\n")

# Testing
print("\nTesting")
test = ['Small', '2-5', -2, 'Yes', 'None', 'B.Tech']
print(test, "is predicted as: ", end="")
print(predict(s_final, test))
