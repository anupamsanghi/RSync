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
	#print content
	client_socket.send(content)
	diff = client_socket.recv(512)
	filelist.insert(0,'')
	#filelist.append('')
	updatelist=diff.splitlines()
	subsplit=[]
	for i in range (0,len(updatelist)):
		subsplit.append(updatelist[i].split('^'))
	print subsplit
	i=0
	while i<len(subsplit):
		if subsplit[i][0]=='-':
			filelist[int(subsplit[i][1])]=''
		elif subsplit[i][0]=='+':
			j=i+1
			string=subsplit[i][2]+'\n'
			while j<len(subsplit) and subsplit[j][1]==subsplit[j-1][1]:
				string=string+subsplit[j][2]+'\n'
				print string
				j+=1
			filelist[int(subsplit[i][1])]=string
			i=j-1
		i+=1
	print filelist
	finalcontent=''.join(filelist)
	print finalcontent
	#file.write(finalcontent)
