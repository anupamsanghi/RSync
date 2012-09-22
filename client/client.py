import socket
import sys


def LCS(X, Y):
    m = len(X)
    n = len(Y)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n+1) for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if X[i-1] == Y[j-1]: 
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C

# for finding only 1 lcs	
def backTrack(C, X, Y, i, j):
    if i == 0 or j == 0:
        return ""
    elif X[i-1] == Y[j-1]:
        return backTrack(C, X, Y, i-1, j-1) + X[i-1]
    else:
        if C[i][j-1] > C[i-1][j]:
            return backTrack(C, X, Y, i, j-1)
        else:
            return backTrack(C, X, Y, i-1, j)


#for finding the difference	
diff=[]	
def createDiff(C, X, Y,i,j, arr):
    global diff
    if i > 0 and j > 0 and X[i-1] == Y[j-1]:
        createDiff(C, X, Y, i-1, j-1,arr)
    else:
        if j > 0 and (i == 0 or C[i][j-1] >= C[i-1][j]):
            createDiff(C, X, Y, i, j-1,arr)
            diff.append("+ " + str(i-1) +" "+ arr[j-1])
        elif i > 0 and (j == 0 or C[i][j-1] < C[i-1][j]):
            createDiff(C, X, Y, i-1, j,arr)
            diff.append("- " + str(i-1) +"\n")

if __name__ == "__main__":
	HOST, PORT = "localhost", 5000
	data = " ".join(sys.argv[1:])

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
	    # Connect to server and send data
	    sock.connect((HOST, PORT))
	    sock.send(data)
	    received = sock.recv(1024)
	except:
		print "Unexpected error:", sys.exec_info()[0]
	#print data
	#print received
	hashlist1=received.split()
	fp=open('doc1','r')
	filelist=[]
	hashlist2=[]
	for line in fp:
		hashlist2.append(str(hash(line)))
		filelist.append(line)
	C = LCS(hashlist1, hashlist2) 
	#print  backTrack(C, hashlist1, hashlist2,len(hashlist1),len(hashlist2))
	createDiff(C, hashlist1, hashlist2,len(hashlist1),len(hashlist2),filelist)
	#print diff
	content=''.join(diff)
	print content
	try:
		sock.send(content)
	except:
		print "Unexpected error:", sys.exec_info()[0]
	finally:
	    sock.close()
