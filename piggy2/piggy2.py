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
    rfound = False
    if ParamVars.IamHead() == True:
        Imode = True
    #while(1):
    #    if not(ParamVars.Error()):
            
            #Create a listning connection
            
            
    piggy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    piggy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if ParamVars.get_noleft() == False:
        piggy.bind(("", 36763))
    piggy.listen(5)
            
            
    
    running = 1
    while running:
        
        if rfound == False:
            piggyr = 0
            rfound = True
            if ParamVars.get_noright() == False and not ParamVars.Error():
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
        inputready, outputready, exceptready = select.select(input, [], [])
        for s in inputready:
            if s == piggy and piggy != 0:
                client, address = piggy.accept()
                input.append(client)
                #Keyboard input
            elif s == sys.stdin:
                message = sys.stdin.readline()
                if message:
                    #doCommand function returns True if message is a command, false otherwise
                    if ParamVars.doCommand(message) == True and Imode == False:
                        if ParamVars.get_noright() == True:
                            try:
                                
                                if piggyr != 0:
                                    piggyr.close()
                                    input.remove(piggyr)
                                    rfound = False
                            except UnboundLocalError, AttributeError:
                                None
                            ParamVars.set_outputl(True)
                            ParamVars.set_outputr(False)
                        if ParamVars.get_noleft() == True:
                            try:
                                if lcon != 0:
                                    lcon.close()
                                    input.remove(lcon)
                            except UnboundLocalError:
                                None
                            ParamVars.set_outputl(False)
                            ParamVars.set_outputr(True)
                        #Double command bug found
                        #message = sys.stdin.readline()
                    if message == "i\n" or Imode == True:
                        if Imode == False:
                            message = sys.stdin.readline()
                        Imode = True
                                
                        #if(not(ParamVars.IamHead())):
                        #   message = sys.stdin.readline()
                        if message.strip() == chr(27):
                            Imode = False
                        else:
                            if(ParamVars.get_loopr() != True and ParamVars.get_loopl() != True):
                                if ParamVars.get_outputr():
                                    if ParamVars.get_loopr():
                                        sendLeft(message, lcon)
                                    else:
                                        sendRight(message, piggyr)
                                if ParamVars.get_outputl(): 
                                    if ParamVars.get_loopl():
                                        sendRight(message, piggyr)
                                    else:
                                        sendLeft(message, lcon)
                                        
            #Recieve from right
            elif s == piggyr and piggyr != 0:
                try:
                    message = s.recv(size)
                except socket.error:
                    print("Connection stopped from the right\n")
                if message != '':
                    if(ParamVars.get_dsprl()):
                        print("Recieve from the right: %s" %message.decode())
                            
                    if(ParamVars.IamMiddle() or ParamVars.IamTail()):
                        if not(ParamVars.get_loopl() and ParamVars.get_loopr()):
                            if ParamVars.get_loopl():
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
                            if(not(ParamVars.get_loopr() and ParamVars.get_loopl())):
                                if ParamVars.get_loopr():
                                    sendLeft(data, s)
                                else:
                                    sendRight(data, piggyr)
                    elif ParamVars.get_loopr():
                        if data:
                            sendLeft(data, s)
                    sys.stdout.flush()
                    



        #elif Eflag == True:
        #    Eflag = False
        #    print("ParameterError: You must include either raddr and/or laddr\n")


if __name__=="__main__":
    main(sys.argv[1:])
