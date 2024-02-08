import numpy as np

with open("../data/test_big_data.txt", 'w') as file:
    file.write("40000 2\n")
    for i in np.arange(-1,1,0.01):
        for j in np.arange(-1,1,0.01):
            file.write("%.1f" % i)
            file.write(" ")
            file.write("%.1f" % j)
            file.write('\n')
            
