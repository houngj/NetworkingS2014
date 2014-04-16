import select, socket, sys, getopt, collections

def main(argv):
    IP = socket.gethostname()
    port = 36763
    size = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sys.stdout.write('%')

    try:
        opts, args = getopt.getopt(argv, "s:dp", ["-s, -p"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in "-s":
            IP=arg
        elif opt in "-p":
            port = int(arg)
    s.connect((IP,port))
    while 1:
        line = sys.stdin.readline()
        if line == ' ':
            break
    
        s.send(line.encode())
        #data = s.recv(size)
        #sys.stdout.write(data.decode())
        #sys.stdout.write('%')

    s.close()

if __name__=="__main__":
    main(sys.argv[1:])


    
