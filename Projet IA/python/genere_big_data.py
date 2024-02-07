import numpy as np

with open("../big_data.txt", 'w') as file:
    file.write("900 2\n")
    for i in np.arange(0,3,0.1):
        for j in np.arange(0,3,0.1):
            file.write("%.1f" % i)
            file.write(" ")
            file.write("%.1f" % j)
            file.write('\n')
            
