import select, socket, sys
from socket import error as SocketError
import errno
host = socket.gethostbyname(socket.gethostname())
port = 36763
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host,port))
server.listen(backlog)
input = [server,sys.stdin]


running = 1
while running:
    inputready, outputready, exceptready = select.select(input,[],[])
    for s in inputready:
        if s == server:
            #handle the server socket
            client, address = server.accept()
            input.append(client)
        elif s == sys.stdin:
            #handle standard input
            junk = sys.stdin.readline()
            running = 0
        else:
            #handle all other sockets
            try:
                data = s.recv(size)
                
                sys.stdout.write(data.decode())
                if data:
                    s.send(data)
                else:
                    s.close()
                    input.remove(s)
            except SocketError as e:
                if e.errno == errno.ECONNRESET:
                    pass
                
                
server.close()
