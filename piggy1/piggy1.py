import select, socket, sys, getopt, collections
import argparse

acctport = 36763
useport = 36763
laddr = None
raddr = None
noleft = False
noright = False
#accept all left address flag
lalladdr = True
#accept all right address flag
ralladdr = True
#accept all right port flag
allacctport = True
#accept all left port flag
alluseport = False

def test():
    global acctport
    global useport
    global laddr
    global raddr
    global noleft
    global noright
    global lalladdr
    global ralladdr
    global allacctport
    global alluseport

    
    
    print("""acctport - %s\n
    allacctport - %s\n
    useport - %d\n
    alluseport - %s\n
    laddr - %s\n
    lalladdr - %s\n
    raddr - %s\n
    ralladdr - %s\n
    noleft - %s\n
    noright - %s\n""" %(acctport, allacctport, useport, alluseport, laddr, lalladdr, raddr, ralladdr, noleft, noright))

def Commandline_Param(argv):
    parser = argparse.ArgumentParser(description="Parse commandline parameters")
    laddr = 0
    parser.add_argument("-laddr", action='store', dest='laddr')
    parser.add_argument("-raddr", action='store', dest='raddr')
    parser.add_argument("-noleft", action='store_true', dest='noleft')
    parser.add_argument("-noright", action='store_true', dest='noright')
    parser.add_argument("-lacctport", action='store', dest='lacctport')
    parser.add_argument("-luseport", action='store', dest='luseport')
    string = " ".join(argv)
    return parser.parse_args(string.split())


def EvalParam(parser):
    global acctport
    global useport
    global laddr
    global raddr
    global noleft
    global noright
    global lalladdr
    global ralladdr
    global allacctport
    global alluseport
    if(parser.laddr != None):
        if(parser.laddr != "*"):
            laddr = parser.laddr
            lalladdr = False
        else:
            #accept all left address flag raised
            lalladdr = True
    
    if(parser.raddr != None):
        if(parser.raddr != "*"):
            ralladdr = False
            raddr = parser.raddr
        else:
            #accept all right address flag raised
            ralladdr = True
    #if -noright was raised in commandline, -raddr option is to be ignored
    if(parser.noright == True):
        noright = True
        raddr = None
        ralladdr = False
    #if -noleft was raised in commandline, -laddr option is to be ignored    
    if(parser.noleft == True):
        noleft = True
        laddr = None
        ralladdr = False
 
    if(parser.lacctport != None):
        if(parser.lacctport != "*"):
            acctport = parser.lacctport
        else:
            allacctport = True
    
    if(parser.luseport != None):
        if(parser.luseport != "*"):
            useport = parser.luseport
            alluseport = False
        else:
            alluseport = True





def main(argv):
    try:
        size = 1024
        parser = Commandline_Param(argv)
        EvalParam(parser)
        
        test()
        
        #if noleft is true then take from keyboard input
        if noleft == False:
            piggyl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            piggyl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #if lalladdr != True:
            #    piggyl.bind((laddr, useport))
            #else:
            piggyl.bind((socket.gethostname(), useport))
            piggyl.listen(5)
            input = [piggyl, sys.stdin]
        if noright == False:
            piggyr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            piggyr.connect((raddr, int(acctport)))
        

        running = 1
        while running:
            
            if (noright == False and noleft == False) or (noright == True and noleft == False):
                inputready, outpuready, exceptready = select.select(input, [],[])
                for s in inputready:
                    
                    if s == piggyl:
                        client, address = piggyl.accept()
                        input.append(client)
                    elif s == sys.stdin:
                        junk = sys.stdin.readline()
                        running = 0
                    else:
                        if s.getpeername()[0] != laddr and laddr != None:
                            s.close()
                            input.remove(s)
                            break
                        data = s.recv(size)
                        
                        
                        
                        print("Recieved %s from %s" %(data.decode(),s.getpeername()))
                        
                        if(noright == False):
                            if data:
                                piggyr.send(data)
                                #recieve message back from server
                                data = piggyr.recv(size)
                                sys.stdout.write(data.decode())
                                if data:
                                    s.send(data)
                                else:
                                    s.close()
                                    input.remove(s)
                            else:
                                s.close()
                                input.remove(s)
                        
                        
                
            elif noright == False and noleft == True:
                #Head piggy so take keyboard input
                line = sys.stdin.readline()
                if line == ' ':
                    break
                
                piggyr.send(line.encode())
                data = piggyr.recv(size)
                print(data.decode())
                print('%')
            else:
            #    print("ParameterError: You must include either raddr or laddr\n")
                break
            
        if (noright == False and noleft == False) or (noright == True and noleft == False):
            piggyl.close()
    except TypeError:
        print("ParameterError: You must include either raddr or laddr\n")
    
        

if __name__=="__main__":
    main(sys.argv[1:])
