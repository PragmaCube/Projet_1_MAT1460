import model

model = model.Model("Distribution selon l'age.csv", 30)

#model.dual_plot([3, 4])

model.multi_plot([3, 3, 4, 4], [0.95, 0.96, 0.95, 0.96])