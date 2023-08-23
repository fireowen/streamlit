import math
import numpy as np

array_size = 101
array = np.zeros((array_size, array_size))

for i in range(array_size):
    for j in range(array_size):
        value = math.sqrt(((50 - i)/10) ** 2 + ((j - 50)/10) ** 2)
        array[i][j] = value

# Print the resulting array
print(array[50][50])