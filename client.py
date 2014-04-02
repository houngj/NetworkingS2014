import select, socket, sys

host = 'localhost'
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
sys.stdout.write('%')

while 1:
    line = sys.stdin.readline()
    if line == ' ':
        break
    s.send(line.encode())
    data = s.recv(size)
    sys.stdout.write(data.decode())
    sys.stdout.write('%')

s.close()



    
