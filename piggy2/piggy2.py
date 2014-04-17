import select, socket, sys
from piggy_util import Param

def main(argv):
    try:
        ParamVars = Param()
        size = 1024
        parser = ParamVars.Commandline_Param(argv)
        ParamVars.EvalParam(parser)
        
        ParamVars.test()
        
        #Create left connection
        if ParamVars.get_noleft() == False:
            piggyl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            piggyl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            piggyl.bind((socket.gethostname(), 36763))
            piggyl.listen(5)
            input = [piggyl, sys.stdin]
        
        #Creat right connection
        if ParamVars.get_noright() == False:
            piggyr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if int(ParamVars.get_useport()) != 36763:
                piggyr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                piggyr.bind((socket.gethostname(), int(ParamVars.get_useport())))
            piggyr.connect((ParamVars.get_raddr(), 36763))

        running = 1
        while running:
            #Either found an end piggy or a middle piggy
            if (ParamVars.get_noright() == False and ParamVars.get_noleft() == False) or (ParamVars.get_noright() == True and ParamVars.get_noleft() == False):
                
                inputready, outpuready, exceptready = select.select(input, [],[])
                for s in inputready:
                    if s == piggyl:
                        client, address = piggyl.accept()
                        input.append(client)
                    elif s == sys.stdin:
                        junk = sys.stdin.readline()
                        running = 0
                    else:
                        if(ParamVars.checkladdr(s) or ParamVars.checkacctport(s)):
                            s.close()
                            input.remove(s)
                            break
                        
                        data = s.recv(size)
                        
                        if(ParamVars.get_dsplr() == True):
                            print("From left side: %s" %data.decode())
                        
                        #found a middle piggy
                        if(ParamVars.get_noright() == False):
                            if data:
                                
                                piggyr.send(data)
                                #recieve message back from server
                                data = piggyr.recv(size)
                                if(ParamVars.get_dsprl() == True):
                                    print("From right side: %s" %data.decode())
                                if data:
                                    #send to left
                                    s.send(data)
                                    
                                        
                                        
                                else:
                                    s.close()
                                    input.remove(s)
                            else:
                                s.close()
                                input.remove(s)
                        #found an end piggy
                        else:
                            if data:
                                s.send(data)
                            else:
                                s.close()
                                input.remove(s)
                        
            #found a head piggy
            elif ParamVars.get_noright() == False and ParamVars.get_noleft() == True:
                
                #Head piggy so take keyboard input
                line = sys.stdin.readline()
                if line == ' ':
                    break
                
                piggyr.send(line.encode())
                data = piggyr.recv(size)
                if(ParamVars.get_dsprl() == True):
                    print("From right side: %s" %data.decode())
                
                
            else:
            
                break
            
        if (ParamVars.get_noright() == False and ParamVars.get_noleft() == False) or (ParamVars.get_noright() == True and ParamVars.get_noleft() == False):
            piggyl.close()
    except TypeError:
        print("ParameterError: You must include either raddr or laddr\n")
    
        

if __name__=="__main__":
    main(sys.argv[1:])
