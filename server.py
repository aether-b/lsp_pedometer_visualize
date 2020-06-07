#!/usr/bin/env python

import socket
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("192.168.0.4", port))
print ("waiting on port 5555")
while 1:
	data, addr = s.recvfrom(1024)
	print (data)
