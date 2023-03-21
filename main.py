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
# Explication des paramètres dans l'ordre :
# 1 - Nombre d'années pour qu'un éléphant naisse (moyenne)
# 2 - Taux de survie des éléphants entre 1 et 60 ans
# 3 - Mise en place de la stratégie
# 4 - Stress causé par le dard (taux de survie en moins)
# 5 - Affichage des moyennes d'éléphants par année
# 6 - Mise en place de la situation de crise : [a t-elle lieu ?, date d'effet, proportion de la population qui survit]
model.multi_plot([3, 3, 4, 4], [0.95, 0.96, 0.95, 0.96], [True, True, True, True], [0.1, 0.1, 0.1, 0.1], [True, True, True, True], [True, 20, 0.1])