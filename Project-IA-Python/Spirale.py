import numpy as np
import pandas as pd
from random import shuffle
import matplotlib.pyplot as plt


def deux_spirales(N=500, rad=2 * np.pi, th0=np.pi / 2):
    N1 = N // 2
    N2 = N - N1

    theta = th0 + np.random.rand(N1) * rad
    spiral1 = np.column_stack((-theta * np.cos(theta) + np.random.rand(N1), theta * np.sin(theta) + np.random.rand(N1)))
    spiral2 = np.column_stack((theta * np.cos(theta) + np.random.rand(N2), -theta * np.sin(theta) + np.random.rand(N2)))

    points = np.vstack((spiral1, spiral2))
    classes = np.concatenate((np.full(N1, 'red'), np.full(N2, 'blue')))

    # Normalisation des données pour qu'elles soient comprises entre -1 et 1
    points = 2 * (points - np.min(points)) / (np.max(points) - np.min(points)) - 1
    temp = []
    for i in range(len(points)):
        temp.append([points[i, 0], points[i, 1], classes[i]])
    shuffle(temp)

    return temp
