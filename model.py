import random
import numpy
import matplotlib.pyplot as plt

total = [0 for i in range(71)]

def sum(list_):
    s = 0
    for elem in list_:
        s += elem

    return s

import csv
    
class Model:
    def __init__(self, csv_file, max_time):
        self.max_time = max_time

        self.distribution_f = []
        self.distribution_m = []
        
        self.sums = []

        self.new_f = 0
        self.new_m = 0

        with open(csv_file, newline='') as csvfile:
            rd = csv.reader(csvfile, delimiter=';', quotechar='|')
            

            for row in rd:
                if row[17] != "Femelles" and row[17] != "":
                    self.distribution_f.append(int(row[17]))

                if row[18] != "Mâles" and row[18] != "":
                    self.distribution_m.append(int(row[18]))

        del self.distribution_f[-1]
        del self.distribution_f[-1]
        del self.distribution_m[-1]
        del self.distribution_m[-1]

        self.distribution_f_base = [] 
        self.distribution_m_base = []

        for i in range(len(self.distribution_f)):
            self.distribution_f_base.append(self.distribution_f[i])
            self.distribution_m_base.append(self.distribution_m[i])

    def twins(self, nbr_f):
        twins_nbr = 0

        for i in range(nbr_f):
            if random.random() < 0.0135:
                twins_nbr += 1

        return twins_nbr

    def simulation(self, birth_mean):
        for time in range(self.max_time):
                for age in range(len(self.distribution_f)):
                    if age < 70:
                        if age == 0:
                            self.distribution_f[age] *= 0.75
                            self.distribution_m[age] *= 0.75
                            #print(str(distribution_m[age]) + " / " + str(distribution_m_temp[age + 1]))

                        elif age < 60:
                            self.distribution_f[age] *= 0.95
                            self.distribution_m[age] *= 0.95
                            #print(distribution_f_temp[age + 1] / distribution_f[age])

                            if age > 11 and age % birth_mean == 0:
                                self.new_f += numpy.floor((self.distribution_f[age] * 2 + self.twins(int(self.distribution_f[age]))) / 2)
                                self.new_m += numpy.floor((self.distribution_f[age] * 2 + self.twins(int(self.distribution_f[age]))) / 2)
                                
                                

                        else:
                            self.distribution_f[age] = self.distribution_f[age] * ((95 - 10 * (self.max_time % 10)) / 100)
                            self.distribution_m[age] = self.distribution_m[age] * ((95 - 10 * (self.max_time % 10)) / 100)

                        self.distribution_f[age] = numpy.floor(self.distribution_f[age])
                        self.distribution_m[age] = numpy.floor(self.distribution_m[age])

                        #distribution_f[age + 1] = distribution_f_temp[age + 1]
                        #print(distribution_m)
                        #distribution_m[age + 1] = distribution_m_temp[age + 1]

                        total[age] = self.distribution_f[age] + self.distribution_m[age]
                        #print(int(distribution_f_temp[age + 1]))
                
                self.distribution_f.pop()
                self.distribution_f.insert(0, self.new_f)
                self.distribution_m.pop()
                self.distribution_m.insert(0, self.new_m)

                self.new_f = self.new_m = 0

                #print(distribution_m)
                #print(distribution_m_temp)

                self.sums.append(sum(total))

                print("Itération " + str(time) + " / Taux : " + str(birth_mean) + " / Nombre : " + str(sum(total)))

    def single_plot(self):
        plt.plot([i for i in range(self.max_time)], self.sums)
        plt.show()
    
    def reset(self):
        for i in range(len(self.distribution_f)):
            self.distribution_f[i] = self.distribution_f_base[i]
            self.distribution_m[i] = self.distribution_m_base[i]

    def dual_plot(self, birth_means):
        self.simulation(birth_means[0])
        plt.plot([i for i in range(self.max_time)], self.sums, color = "r", label = f"1 éléphant / {str(birth_means[0])} ans")

        self.sums.clear()
        self.reset()

        self.simulation(birth_means[1])
        plt.plot([i for i in range(self.max_time)], self.sums, color = "g", label = f"1 éléphant / {str(birth_means[1])} ans")

        plt.xlabel("Années écoulées")
        plt.ylabel("Nombre d'éléphants")
        plt.title("Comparaison selon différents taux")
        plt.legend()

        plt.show()

