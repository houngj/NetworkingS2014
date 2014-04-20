import select, socket, sys
from piggy_util import Param

def main(argv):

    ParamVars = Param()
    size = 1024
    parser = ParamVars.Commandline_Param(argv)
    ParamVars.EvalParam(parser)
    ParamVars.test()
    Eflag = True
    Imode = False
    while(1):
        if not(ParamVars.Error()):            
            #Create a listning connection
            piggy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            piggy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            piggy.bind((socket.gethostname(), 36763))
            piggy.listen(5)
            
            
            piggyr = 0
            if ParamVars.get_noright() == False:
                #Create send connection
                piggyr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if int(ParamVars.get_useport()) != 36763:
                    piggyr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    piggyr.bind((socket.gethostname(), int(ParamVars.get_useport())))
                piggyr.connect((ParamVars.get_raddr(), 36763))
            #if(ParamVars.get_noleft == False and ParamVars.get_noright == False):
            input = [piggy, sys.stdin, piggyr]
            #else:
            #    input = [piggy, sys.stdin]
            running = 1
            while running:
                inputready, outputready, exceptready = select.select(input, [], [])
                for s in inputready:
                    if s == piggy:
                        client, address = piggy.accept()
                        input.append(client)
                    #Keyboard input
                    elif s == sys.stdin:
                        
                        message = sys.stdin.readline()
                        if message:
                            if message == "i\n" or Imode or ParamVars.IamHead():
                                Imode = True
                                #if(not(ParamVars.IamHead())):
                                #   message = sys.stdin.readline()
                                if message == "exit!\n":
                                    Imode = False
                                else:
                                    if ParamVars.outputr:
                                        piggyr.send(message)
                                    else:
                                        lcon.send(message)
                                
                    #Recieve from right
                    elif s == piggyr and piggyr != 0:
                        
                        message = s.recv(size)
                        if message != '':
                            if(ParamVars.get_dsprl()):
                                print("Recieve from the right: %s" %message.decode())
                            
                            if(ParamVars.IamMiddle() or ParamVars.IamTail()):
                                lcon.send(message)
                        else:
                            break
                    #recieve from left
                    elif s != 0:
                        lcon = s
                        if(ParamVars.checkladdr(s) or ParamVars.checkacctport(s)):
                            print("Connection rejected")
                            s.close()
                            input.remove(s)
                            break
                        
                        data = s.recv(size)
                        
                        if data:
                            if(ParamVars.get_dsplr() == True):
                                print("From left side: %s" %data.decode())
                        
                            if(ParamVars.IamHead() or ParamVars.IamMiddle()):
                                if data:
                                    piggyr.send(data)
                            else:
                                if data:
                                    s.send(data)
                            sys.stdout.flush()
                    



        elif Eflag == True:
            Eflag = False
            print("ParameterError: You must include either raddr and/or laddr\n")


if __name__=="__main__":
    main(sys.argv[1:])
