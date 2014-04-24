import select, socket, sys
from piggy_util import *
def main(argv):

    ParamVars = Param()
    size = 1024
    parser = ParamVars.Commandline_Param(argv)
    ParamVars.EvalParam(parser)
    ParamVars.test()
    Eflag = True
    Imode = False
    lcon = 0
    if ParamVars.IamHead() == True:
        Imode = True
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
                            if ParamVars.doCommand(message) == True and Imode == False:
                                if ParamVars.get_noright() == True:
                                    try:
                                        piggyr.close()
                                        input.remove(piggyr)
                                    except UnboundLocalError:
                                        None
                                    ParamVars.set_outputl(True)
                                    ParamVars.set_outputr(False)
                                if ParamVars.get_noleft() == True:
                                    try:
                                        lcon.close()
                                        input.remove(lcon)
                                    except UnboundLocalError:
                                        None
                                    ParamVars.set_outputl(False)
                                    ParamVars.set_outputr(True)
                                message = sys.stdin.readline()
                            if message == "i\n" or Imode == True:
                                if Imode == False:
                                    message = sys.stdin.readline()
                                Imode = True
                                
                                #if(not(ParamVars.IamHead())):
                                #   message = sys.stdin.readline()
                                if message.strip() == chr(27):
                                    Imode = False
                                else:
                                    if ParamVars.get_outputr():
                                        if ParamVars.get_loopl:
                                            sendLeft(message, lcon)
                                        else:
                                            sendRight(message, piggyr)
                                    if ParamVars.get_outputl(): 
                                        if ParamVars.get_loopr:
                                            sendRight(message, piggyr)
                                        else:
                                            sendLeft(message, lcon)
                                        
                    #Recieve from right
                    elif s == piggyr and piggyr != 0:
                        message = s.recv(size)
                        if message != '':
                            if(ParamVars.get_dsprl()):
                                print("Recieve from the right: %s" %message.decode())
                            
                            if(ParamVars.IamMiddle() or ParamVars.IamTail()):
                                if ParamVars.get_loopr():
                                    sendRight(message, piggyr)
                                else:
                                    sendLeft(message, lcon)
                                    
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
                        try:
                            data = s.recv(size)
                            if data == "":
                                s.close()
                                input.remove(s)
                        except socket.error:
                            print("Connection stopped from the left\n")

                        if data:
                            if(ParamVars.get_dsplr() == True):
                                print("From left side: %s" %data.decode())
                            
                            if(ParamVars.IamHead() or ParamVars.IamMiddle()):
                                if data:
                                    if ParamVars.get_loopl():
                                        sendLeft(data, s)
                                    else:
                                        sendRight(data, piggyr)
                            else:
                                if data:
                                    sendLeft(data, s)
                            sys.stdout.flush()
                    



        elif Eflag == True:
            Eflag = False
            print("ParameterError: You must include either raddr and/or laddr\n")


if __name__=="__main__":
    main(sys.argv[1:])
