# from pwn import *

# context.log_level = 'error'

# i = 10
# while True:
#   p = remote("52.59.124.14", port=5016)

#   p.sendline(b'1')
#   p.sendline(str(34716455).encode())
#   p.sendline(b'1')
#   p.sendline(b'2')
#   print(f'{i}:   {p.recvall().strip().decode()}')
#   p.close()

#   i += 1
#   break

from math import sqrt
import numpy as np


# a = int(34716455.0)

# power = np.zeros(1, dtype=np.int32)
# power[0] = int(a)
# power = power ** 2
# print(power)

for i in range(1, 4198401):
  a = sqrt(-15 + (2**32)*i)
  # print(f'i = {i}, a = {a}')
  if (a - int(a)) == 0:
    print(i)
