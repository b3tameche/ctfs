from pwn import *

context.clear(arch='amd64')
context.log_level = 'error'

flag_enc = "02 92 a8 06 77 a8 32 3f 15 68 c9 77 de 86 99 7d 08 60 8e 64 77 be ba 74 26 96 e7 4e".split()

start = "BITSCTF"

inject = start
index = len(start)
while True:
  for i in range(33, 127):
    curr = inject + chr(i)
    p = process(f"./loginator.out {curr}", shell=True)
    content = p.recvall().strip().decode().split()
    print(f'current: {curr}')
    print(f'content: {content}')
    if len(content) == 0:
      continue
    if content[-1] == flag_enc[index]:
      inject = curr
      index += 1
      break
  
  if len(inject) == 28:
    break

print(inject)
