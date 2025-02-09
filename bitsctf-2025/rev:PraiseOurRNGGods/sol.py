from pwn import *
from randcrack import RandCrack

trials = 625
xorxe = 412802356
multiplier = 2969596945

conn = remote('chals.bitskrieg.in', port=7007)

rc = RandCrack()

conn.recvuntil(b'> ')
conn.sendline((b'0\n'*(trials-1))[:-1])
lines = conn.recvlines(trials-1)

def transform(line: bytes):
  return int(line.decode().strip('> ').split()[4]) # difference

differences = list(map(transform, lines))

for i in range(1, trials):
  divisor = (i ^ xorxe) * multiplier
  sample = differences[i-1] // divisor
  rc.submit(sample)

predbits = rc.predict_getrandbits(32)
predpass = (trials ^ xorxe) * multiplier * predbits

conn.sendline(f'{predpass}'.encode())
print(conn.recvall(timeout=1).decode())

conn.close()
