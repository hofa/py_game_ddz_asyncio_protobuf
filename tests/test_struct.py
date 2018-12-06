import struct
command = 0x0001
length = 123456

data = struct.pack("II", command, length)
print(data)
command, length = struct.unpack("II", data)
print(command, length)