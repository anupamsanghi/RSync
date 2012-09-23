import socket
import os

if __name__ == "__main__":
	#creating server socket
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("", 5000))
	server_socket.listen(5)
	print "TCPServer Waiting for client on port 5000"
	client_socket, address = server_socket.accept()
	print "I got a connection from ", address
        data = client_socket.recv(512)
	print data
	file=open(data,'r+')
	filelist=[]
	hashlist=[]
	for line in file:
		filelist.append(line)
		hashlist.append(str(hash(line)))
	content=' '.join(hashlist)
	client_socket.send(content)
	diff = client_socket.recv(512)
	updatelist=diff.splitlines()
	subsplit=[]
	for i in range (0,len(updatelist)):
		subsplit.append(updatelist[i].split('^'))
	print subsplit
	for element in subsplit:
		if element[0]=='-':
			filelist[int(element[1])]=''
		elif element[0]=='+':
			filelist[int(element[1])]=element[2]
	print filelist
	finalcontent=''.join(filelist)
	print finalcontent
