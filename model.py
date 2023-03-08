# On ajoute ce module pour les jumeaux
import random

# On ajoute ce module pour faire l'arrondi par défaut
import numpy

# Pour la visualisation
import matplotlib.pyplot as plt

# Pour lire les données dans un fichier csv
import csv

total = [0 for i in range(71)]

def sum(list_):
    s = 0
    for elem in list_:
        s += elem

    return s
    
class Model:
    def __init__(self, csv_file, max_time, display = False):
        self.max_time = max_time
        self.display = display

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

        # On retire les deux derniers éléments puisque qu'ils ne contiennent
        # pas les données voulues.
        del self.distribution_f[-1]
        del self.distribution_f[-1]
        del self.distribution_m[-1]
        del self.distribution_m[-1]

        self.distribution_f_base = [] 
        self.distribution_m_base = []

        # On garde en mémoire les valeurs initiales pour potentiellement
        # faire d'autres simulations.
        for i in range(len(self.distribution_f)):
            self.distribution_f_base.append(self.distribution_f[i])
            self.distribution_m_base.append(self.distribution_m[i])

    def reset(self):
        for i in range(len(self.distribution_f)):
            self.distribution_f[i] = self.distribution_f_base[i]
            self.distribution_m[i] = self.distribution_m_base[i]

        self.sums.clear()

    def twins(self, nbr_f):
        twins_nbr = 0

        for i in range(nbr_f):
            if random.random() < 0.0135:
                twins_nbr += 1

        return twins_nbr

    def simulation(self, birth_mean, survival_rate = 0.95):
        for time in range(self.max_time):
                for age in range(len(self.distribution_f)):
                    if age < 70:
                        if age == 0:
                            self.distribution_f[age] *= 0.75
                            self.distribution_m[age] *= 0.75

                        elif age < 60:
                            self.distribution_f[age] *= survival_rate
                            self.distribution_m[age] *= survival_rate

                            if age > 11 and age % birth_mean == 0:
                                self.new_f += numpy.floor((self.distribution_f[age] * 2 + self.twins(int(self.distribution_f[age]))) / 2)
                                self.new_m += numpy.floor((self.distribution_f[age] * 2 + self.twins(int(self.distribution_f[age]))) / 2)
                                
                                

                        else:
                            # Lorsque l'éléphant a plus de 60 ans, son taux de survie décroit linéairement.
                            self.distribution_f[age] = self.distribution_f[age] * ((95 - 10 * (self.max_time % 10)) / 100)
                            self.distribution_m[age] = self.distribution_m[age] * ((95 - 10 * (self.max_time % 10)) / 100)

                        self.distribution_f[age] = numpy.floor(self.distribution_f[age])
                        self.distribution_m[age] = numpy.floor(self.distribution_m[age])

                        total[age] = self.distribution_f[age] + self.distribution_m[age]
                
                # On déplace les éléments de chaque liste vers la droite.
                self.distribution_f.pop()
                self.distribution_f.insert(0, self.new_f)
                self.distribution_m.pop()
                self.distribution_m.insert(0, self.new_m)

                self.new_f = self.new_m = 0

                self.sums.append(sum(total))

                if self.display:
                    print("Itération " + str(time) + " / Taux : " + str(birth_mean) + " / Nombre : " + str(sum(total)))

    def single_plot(self):
        plt.plot([i for i in range(self.max_time)], self.sums)
        plt.show()

    def dual_plot(self, birth_means):
        self.simulation(birth_means[0])
        plt.plot([i for i in range(self.max_time)], self.sums, label = f"1 éléphant / {str(birth_means[0])} ans")

        self.reset()

        self.simulation(birth_means[1])
        plt.plot([i for i in range(self.max_time)], self.sums, label = f"1 éléphant / {str(birth_means[1])} ans")

        plt.xlabel("Années écoulées")
        plt.ylabel("Nombre d'éléphants")
        plt.title("Comparaison selon différents taux")
        plt.legend()

        plt.show()

    def multi_plot(self, birth_means, survival_rates):
        if len(birth_means) != len(survival_rates):
            return False

        for i in range(len(birth_means)):
            self.reset()

            self.simulation(birth_means[i], survival_rates[i])
            plt.plot([i for i in range(self.max_time)], self.sums, label = f"1 éléphant / {str(birth_means[i])} ans | S = {survival_rates[i]}")

        plt.xlabel("Années écoulées")
        plt.ylabel("Nombre d'éléphants")
        plt.title("Comparaison selon différents taux")
        plt.legend()

        plt.show()