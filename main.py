# Note : plusieurs fois dans le programme on réinitialisera
# des listes en les parcourant entièrement (et donc en changeant
# un à un les éléments de celles-ci) au lieu de simplement les
# réinitialiser avec une liste stockant les conditions initiales.
# Ceci est dû au fait que les listes se comportent de manière
# aux pointeurs. On veut donc éviter de manipuler la même adresse
# pour garder des valeurs distinctes.

import model

model = model.Model("Distribution selon l'age.csv", 65, False, [0, 0])

#model.dual_plot([3, 4])

# On fait ici 8 simulations pour tester l'influence de 3 paramètres différents
model.multi_plot([3, 3, 4, 4], [0.95, 0.96, 0.95, 0.96], [True, True, True, True], [0.1, 0.1, 0.1, 0.1], [True, True, True, True], [False, 10, 0.3])