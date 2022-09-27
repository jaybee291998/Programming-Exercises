# file = open('bin_file.bin', 'wb')
# sentence = bytearray("this is good".encode('ascii'))
# file.write(sentence)
# file.close()

file = open('bin_file.bin', 'rb')
b = file.read()
print(type(byte(b[0])))
file.close()

