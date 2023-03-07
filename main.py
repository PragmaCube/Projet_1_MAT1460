import random
import numpy
import matplotlib.pyplot as plt

distribution_f = []
distribution_m = []

sums = []

new_f = 0
new_m = 0

distribution_f_temp = [0 for i in range(71)]
distribution_m_temp = [0 for i in range(71)]

total = [0 for i in range(71)]

import csv

with open("Distribution selon l'age.csv", newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:

        if row[17] != "Femelles" and row[17] != "":
            distribution_f.append(int(row[17]))

        if row[18] != "Mâles" and row[18] != "":
            distribution_m.append(int(row[18]))
        
    del distribution_f[-1]
    del distribution_f[-1]
    del distribution_m[-1]
    del distribution_m[-1]
    
#print(distribution_f)
#print(distribution_m)

def sum(list_):
    s = 0
    for elem in list_:
        s += elem

    return s

def twins(nbr_f):
    twins_nbr = 0

    for i in range(nbr_f):
        if random.random() < 0.0135:
            twins_nbr += 1

    return twins_nbr

for time in range(30):
        for age in range(len(distribution_f)):
            if age < 70:
                if age == 0:
                    distribution_f[age] *= 0.75
                    distribution_m[age] *= 0.75
                    #print(str(distribution_m[age]) + " / " + str(distribution_m_temp[age + 1]))

                elif age < 60:
                    distribution_f[age] *= 0.95
                    distribution_m[age] *= 0.95
                    #print(distribution_f_temp[age + 1] / distribution_f[age])

                    if age > 11 and age % 3 == 0:
                        new_f += numpy.floor((distribution_f[age] * 2 + twins(int(distribution_f[age]))) / 2)
                        new_m += numpy.floor((distribution_f[age] * 2 + twins(int(distribution_f[age]))) / 2)
                        
                        

                else:
                    distribution_f[age] = distribution_f[age] * ((95 - 10 * (time % 10)) / 100)
                    distribution_m[age] = distribution_m[age] * ((95 - 10 * (time % 10)) / 100)

                distribution_f[age] = numpy.floor(distribution_f[age])
                distribution_m[age] = numpy.floor(distribution_m[age])

                #distribution_f[age + 1] = distribution_f_temp[age + 1]
                #print(distribution_m)
                #distribution_m[age + 1] = distribution_m_temp[age + 1]

                total[age] = distribution_f[age] + distribution_m[age]
                #print(int(distribution_f_temp[age + 1]))
        
        distribution_f.pop()
        distribution_f.insert(0, new_f)
        distribution_m.pop()
        distribution_m.insert(0, new_m)

        new_f = new_m = 0

        #print(distribution_m)
        #print(distribution_m_temp)

        sums.append(sum(total))

        print(sum(total))

        
#print(distribution_f)

plt.plot([i for i in range(30)], sums)
plt.show()