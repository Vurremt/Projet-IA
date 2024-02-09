import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def deux_spirales(N=500, rad=2*np.pi, th0=np.pi/2):
    N1 = N // 2
    N2 = N - N1

    theta = th0 + np.random.rand(N1) * rad
    spiral1 = np.column_stack((-theta * np.cos(theta) + np.random.rand(N1), theta * np.sin(theta) + np.random.rand(N1)))
    spiral2 = np.column_stack((theta * np.cos(theta) + np.random.rand(N2), -theta * np.sin(theta) + np.random.rand(N2)))

    points = np.vstack((spiral1, spiral2))
    classes = np.concatenate((np.full(N1, 'Rouge'), np.full(N2, 'Bleu')))

    # Normalisation des données pour qu'elles soient comprises entre -1 et 1
    points = 2 * (points - np.min(points)) / (np.max(points) - np.min(points)) - 1

    with open("../data/spiral_data_fit.txt", 'w') as file:
        file.write(str(N))
        file.write(" 2 1\n")
        x = points[:, 0]
        y = points[:, 1]
        for i in range(0,N//2):
            file.write("%.3f" % x[i])
            file.write(" ")
            file.write("%.3f" % y[i])
            file.write(" ")
            if classes[i] == 'Rouge' :
                file.write("1")
                file.write("\n")
            else:
                file.write("0" % y[(N//2)+i])
                file.write("\n")
            file.write("%.3f" % x[(N//2)+i])
            file.write(" ")
            file.write("%.3f" % y[(N//2)+i])
            file.write(" ")
            if classes[(N//2)+i] == 'Rouge' :
                file.write("1")
                file.write("\n")
            else:
                file.write("0" % y[(N//2)+i])
                file.write("\n")
    

    return pd.DataFrame({'x1': points[:, 0], 'x2': points[:, 1], 'class': classes})

np.random.seed(42)
spiral = deux_spirales()
        

# Graphiquement :
colors = {'Rouge': 'red', 'Bleu': 'blue'}
plt.scatter(spiral['x1'], spiral['x2'], c=spiral['class'].map(colors))
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.show()
