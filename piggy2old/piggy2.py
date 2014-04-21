import select, socket, sys
from piggy_util import Param


def main(argv):
    
    ParamVars = Param()
    size = 1024
    parser = ParamVars.Commandline_Param(argv)
    ParamVars.EvalParam(parser)
    Eflag = True
    ParamVars.test()
    Imode = False
    lside = None
    while(1):
        
        if not(ParamVars.Error()):
            
            #Create left connection
            #if ParamVars.get_noleft() == False:
                
            piggyl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            piggyl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            piggyl.bind((socket.gethostname(), 36763))
            piggyl.listen(5)
            input = [piggyl, sys.stdin]
            outputs = []
                #Creat right connection
            if ParamVars.get_noright() == False:
                piggyr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if int(ParamVars.get_useport()) != 36763:
                    piggyr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    piggyr.bind((socket.gethostname(), int(ParamVars.get_useport())))
                piggyr.connect((ParamVars.get_raddr(), 36763))
            
            running = 1
            lcon = None
            while running:
                inputready, outputready, exceptready = select.select(input, outputs, [])
                for s in inputready:
                    if s == piggyl:
                        client, address = piggyl.accept()
                        input.append(client)
                        outputs.append(client)
                    elif s == sys.stdin:
                        message = sys.stdin.readline()
                        if(ParamVars.get_noleft == True):
                            piggyr.send(message)
                    elif s == piggyr:
                        message = s.recv(size)
                        if(ParamVars.get_noleft == True):
                            if(ParamVars.get_dsprl()):
                                print("Recieve from the left %s" %message.decode())
                        else:
                            if(ParamVars.get_dsplr()):
                                print("Recieve from the right %s" %message.decode())
                            lcon.send(message)
                            
                    else:
                        lcon = s
                        if(ParamVars.checkladdr(s) or ParamVars.checkacctport(s)):
                            print("Connection rejected")
                            s.close()
                            input.remove(s)
                            break
                        message = s.recv(size)
                        if(ParamVars.get_noright == True):
                            if(ParamVars.get_dsplr()):
                                print("Recieve from the left %s" %message.decode())
                                s.send(message)
                        else:
                            if(ParamVars.get_dsplr()):
                                print("Recieve from right %s" %message.decode())
                                piggyr.send(message)
                            
                            
                            
                            
                            
                        
                
                
            
            if (ParamVars.get_noright() == False and ParamVars.get_noleft() == False) or (ParamVars.get_noright() == True and ParamVars.get_noleft() == False):
                piggyl.close()
        elif Eflag == True:
            Eflag = False
            print("ParameterError: You must include either raddr and/or laddr\n")
    
        

if __name__=="__main__":
    main(sys.argv[1:])
