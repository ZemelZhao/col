
import numpy as np
import multiprocessing as mp
import time

a = np.arange(100000).reshape(-1, 1)
b = np.arange(1000).reshape(-1, 1)

c = mp.Array('d', a)
d = mp.Array('d', b)

time_start = time.time()
e = np.frombuffer(c.get_obj())
print(time.time() - time_start)

time_start = time.time()
f = np.frombuffer(d.get_obj())
print(time.time() - time_start)

time_start = time.time()
g = c[:]
print(time.time() - time_start)

