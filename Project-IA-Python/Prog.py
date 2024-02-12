import numpy as np

from Reseau import *
from Spirale import *

import array

np.random.seed(43)
N = 250
spirale = deux_spirales(N, 2 * np.pi, np.pi / 2)

xData = []
yData = []
for i in range(N):
    print(spirale[i][0], spirale[i][1],spirale[i][2])
    xData.append([spirale[i][0], spirale[i][1]])
    if spirale[i][2] == 'red' :
        yData.append(1)
    else:
        yData.append(0)

model = Network()
model.addLayer( Linear(2, 30) )
model.addLayer( Sigmoid() )
model.addLayer( Linear(30, 1 ))
model.addLayer( Sigmoid() )

model.fit(xData, yData, 100000, 0.01)


# Affichage

plan = []
plan_x = []
plan_y = []
for i in np.arange(-1,1,0.05):
        for j in np.arange(-1,1,0.05):
            plan.append([i,j])
            plan_x.append(i)
            plan_y.append(j)
result = model.feedforward(plan)
result_blue_red = [('blue' if i < 0.5 else 'red') for i in result]
plt.scatter(plan_x, plan_y, c=result_blue_red, marker=".")

spiraleX = []
spiraleY = []
spiraleColor = []
for i in range(N):
    spiraleX.append(spirale[i][0])
    spiraleY.append(spirale[i][1])
    spiraleColor.append(spirale[i][2])
plt.scatter(spiraleX, spiraleY, c=spiraleColor)

plt.show()
