# On ajoute ce module pour les jumeaux
import random

# On ajoute ce module pour faire l'arrondi par défaut
import numpy

# Pour la visualisation
import matplotlib.pyplot as plt

# Pour lire les données dans un fichier csv
import csv

total = [0 for i in range(71)]

# On ajoute cette fonction pour alléger le programme
def sum(list_):
    s = 0
    for elem in list_:
        s += elem

    return s
    
# La classe contenant le coeur du programme. 
class Model:
    def __init__(self, csv_file, max_time, display = False, cannot_breed = [0, 0]):
        self.max_time = max_time
        self.display = display

        self.elephants = []

        self.elephants_f_process = []
        self.elephants_m = []
        
        self.elephants_f_free = []
        self.administration_status = 0

        self.sums = []

        self.new_f = 0
        self.new_m = 0

        # Lecture des données contenues dans le csv. De cette façon,
        # il suffit de mettre à jour le csv pour avoir de nouvelles
        # conditions initiales.
        with open(csv_file, newline='') as csvfile:
            rd = csv.reader(csvfile, delimiter=';', quotechar='|')

            for row in rd:
                if row[17] != "Femelles" and row[17] != "":
                    self.elephants_f_free.append(int(row[17]))

                if row[18] != "Mâles" and row[18] != "":
                    self.elephants_m.append(int(row[18]))

        # On retire les deux derniers éléments puisque qu'ils ne contiennent
        # pas les données voulues.
        del self.elephants_f_free[-1]
        del self.elephants_f_free[-1]
        del self.elephants_m[-1]
        del self.elephants_m[-1]

        self.elephants_f_base = [] 
        self.elephants_m_base = []

        # On garde en mémoire les valeurs initiales pour potentiellement
        # faire d'autres simulations.
        for i in range(len(self.elephants_f_free)):
            self.elephants_f_base.append(self.elephants_f_free[i])
            self.elephants_m_base.append(self.elephants_m[i])
            self.elephants_f_process.append(0)

        self.elephants_f_free[cannot_breed[0]] -= cannot_breed[1]

        # Nombre initial d'éléphants dans la simulation.
        #print(sum(self.elephants_m) + sum(self.elephants_f_free))


    # Ici, bien que cette fonction correspond à l'administration d'un dard,
    # il faut plutôt l'interpréter de cette manière :
    # Elle est appelée avec le paramètre True si l'on souhaite déplacer les
    # éléphants de la liste elephants_f_process vers elephants_f_free. Cela
    # veut dire que les éléphants n'ont pas de nouveau dard administré pour
    # l'année.
    # Elle est appelée avec le paramètre False si l'on souhaite faire le
    # contraire, c'est-à-dire administrer un dard aux éléphants femelles
    # entre 11 et 60 ans.
    # Si elle n'est pas appelée mais que les éléphants sont toujours dans
    # elephants_f_process, cela veut dire qu'un nouveau dard est administré
    # aux femelles entre 11 et 60. Par ailleurs, il est très possible que 
    # certaines femelles ayant plus de 60 ans aient toujours un dard (elles
    # sont toujours dans elephants_f_process). Cependant, elle ne seront pas
    # comptabilisées ainsi, puisque l'on s'assure (voir plus bas) que seules
    # les femelles entre 11 et 60 ans dans elephants_f_process subissent les
    # conséquences de l'administration (stress supplémentaire).
    def transfertAll(self, administration):
        if administration:
            for age in range(11, len(self.elephants_f_free), 59):
                if self.elephants_f_process[age] != 0:
                    self.elephants_f_free[age] = self.elephants_f_process[age]
                    self.elephants_f_process[age] = 0

        else:
            for age in range(11, len(self.elephants_f_free), 59):
                if self.elephants_f_free[age] != 0:
                    self.elephants_f_process[age] = self.elephants_f_free[age]
                    self.elephants_f_free[age] = 0
    
    # On réinitialise les listes utilisées en fonction des conditions initiales.
    def reset(self):
        for i in range(len(self.elephants_f_free)):
            self.elephants_f_process[i] = 0
            self.elephants_f_free[i] = self.elephants_f_base[i]
            self.elephants_m[i] = self.elephants_m_base[i]

        self.sums.clear()

    # On calcule le nombre de jumeaux donnés par nbr_f femelles.
    def twins(self, nbr_f):
        twins_nbr = 0

        for i in range(nbr_f):
            if random.random() < 0.0135:
                twins_nbr += 1

        return twins_nbr

    # On calcule le nombre de morts en fonction de l'âge des éléphants.
    def death(self, nbr, probability):
        death = 0

        for i in range(nbr):
            if random.random() > probability:
                death += 1

        return death

    def simulation(self, birth_mean, survival_rate = 0.95, administration = False, stress_rate = 0.1):
        # Les morts chez les mâles, les femelles avec un dard et celles sans.
        f_process_death = 0
        f_free_death = 0
        m_death = 0

        # On veut éviter que des femelles puissent se reproduire directement
        # après que l'administration du dard ait pris fin. On conserve ainsi 
        # le fait qu'une femelle n'ait qu'un éléphant au bout de birth_mean 
        # ans.
        years_since_administration = 0

        for time in range(self.max_time):
            for age in range(len(self.elephants_f_free)):
                if age >= 70:
                    # Si les éléphants ont 70 ans ou plus, ils meurent
                    self.elephants_f_free[age] = 0
                    self.elephants_f_process[age] = 0
                    self.elephants_m[age] = 0

                elif age < 1:
                    # Les éléphants ayant moins d'un an survivent dans 75% des cas.
                    f_process_death = self.death(self.elephants_f_process[age], 0.75)
                    f_free_death = self.death(self.elephants_f_free[age], 0.75)
                    m_death = self.death(self.elephants_m[age], 0.75)

                    self.elephants_f_process[age] -= f_process_death
                    self.elephants_f_free[age] -= f_free_death
                    self.elephants_m[age] -= m_death

                elif age < 60:
                    # Les éléphants ayant moins de 60 ans survivent dans survival_rate * 100 % des cas.
                    f_process_death = self.death(self.elephants_f_process[age], survival_rate - stress_rate)
                    f_free_death = self.death(self.elephants_f_free[age], survival_rate)
                    m_death = self.death(self.elephants_m[age], survival_rate)

                    self.elephants_f_process[age] -= f_process_death
                    self.elephants_f_free[age] -= f_free_death
                    self.elephants_m[age] -= m_death

                    # Les femelles se reproduisent si elles ont au moins 11 ans et tout les birth_mean
                    # après avoir reçu une administration (ou pas). À noter que si rien ne se passe 
                    # (pas d'administration de dard), les femelles ne se reproduiront qu'à partir de 
                    # birth_mean années après le début de la simulation.
                    if age >= 11:
                        if administration and years_since_administration % birth_mean == 0 and years_since_administration != 0: 
                            self.new_f += int(numpy.floor((self.elephants_f_free[age] * 2 + self.twins(int(self.elephants_f_free[age]))) / 2))
                            self.new_m += int(numpy.floor((self.elephants_f_free[age] * 2 + self.twins(int(self.elephants_f_free[age]))) / 2))
                        
                        elif not administration and age % birth_mean == 0:
                            self.new_f += int(numpy.floor((self.elephants_f_free[age] * 2 + self.twins(int(self.elephants_f_free[age]))) / 2))
                            self.new_m += int(numpy.floor((self.elephants_f_free[age] * 2 + self.twins(int(self.elephants_f_free[age]))) / 2))

                else:
                    # Les éléphants ayant plus de 60 ans ont un taux de survie qui diminue linéairement
                    # en fonction de l'âge.
                    f_process_death = self.death(self.elephants_f_process[age], (100 * (survival_rate) - 10 * (time % 10)) / 100)
                    f_free_death = self.death(self.elephants_f_free[age], (survival_rate * 100 - 10 * (time % 10)) / 100)
                    m_death = self.death(self.elephants_m[age], (survival_rate * 100 - 10 * (time % 10)) / 100)

                    self.elephants_f_process[age] -= f_process_death
                    self.elephants_f_free[age] -= f_free_death
                    self.elephants_m[age] -= m_death

                # On fait le total des listes pour avoir le nombre d'éléphants total.
                total[age] = self.elephants_f_process[age] + self.elephants_m[age] + self.elephants_f_free[age]
                
            # On déplace les éléments de chaque liste vers la droite.
            self.elephants_f_process.pop()
            self.elephants_f_process.insert(0, 0)
            self.elephants_m.pop()
            self.elephants_m.insert(0, self.new_m)
            self.elephants_f_free.pop()
            self.elephants_f_free.insert(0, self.new_f)

            self.new_f = self.new_m = 0

            self.sums.append(sum(total))

            # S'il y a trop d'éléphants, un dard est administré.
            if administration:
                if sum(total) > 10300:
                    self.transfertAll(False)
                    years_since_administration = 0

                # S'il y a trop peu d'éléphants, l'administration prend fin.
                elif sum(total) < 7200:
                    self.transfertAll(True)
                    years_since_administration = 0

                else:
                    years_since_administration += 1

            if self.display:
                print(f"elephants_f_process : {sum(self.elephants_f_process)}, elephants_f_free : {sum(self.elephants_f_free)}, elephants_m : {sum(self.elephants_m)}")

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

    def multi_plot(self, birth_means, survival_rates, administration, stress_rates):
        if len(birth_means) != len(survival_rates):
            return False

        for i in range(len(birth_means)):
            self.reset()

            self.simulation(birth_means[i], survival_rates[i], administration[i], stress_rates[i])
            plt.plot([i for i in range(self.max_time)], self.sums, label = f"1 éléphant / {str(birth_means[i])} ans | S = {survival_rates[i]} | sr = {stress_rates[i]}")
            print(sum(self.sums) / self.max_time)

        plt.xlabel("Années écoulées")
        plt.ylabel("Nombre d'éléphants")
        plt.title("Comparaison selon différents taux")
        plt.legend()

        plt.show()