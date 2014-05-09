import select, socket, sys, curses, time
from piggy_util import *

class window:
    
    def __init__(self):
        self.box = None
        self.row = 1
        
    def set_win(self, box):
        self.box = box
        
    
    def get_win(self):
        return self.box
    
    def get_row(self):
        return self.row
        
    def add_row(self):
        self.row = self.row+1
        
    def set_row(self, num):
        self.row = num

def sendLeft(message, lcon, errwin):
    try:
        if lcon != 0:
            lcon.send(message)
    except:
        errwin.get_win().addstr(1, 1, "no connection to the Left\n")
        errwin.get_win().refresh()
def sendRight(message, rcon, errwin):
    try:
        rcon.send(message)
    except:
        errwin.get_win().addstr(1, 1, "No connection to the Right\n")    
        errwin.get_win().refresh()

def typed(windows):
    windows.get_win().clear()
    windows.get_win().border(0)
    windows.get_win().refresh()
    col = 1
    row = 1
    buff = []
    
    while(1):
        win = windows.get_win()
        ch = win.getch()
        
        
        if (ch < 32 and ch != 13 and ch != 27):
            
            ch = int(ch)
            win.addstr(row, col, str(ch))
            buff.append(str(ch))
            col = col+1
        else:
            win.addch(row, col, ch)
            buff.append(chr(ch))
    
        
        #detect for enter, i, or esc
        if ch == 13 or (chr(ch) == "i" and buff[0] == "i") or (chr(ch) == chr(27) and buff[0] == chr(27)):
            win.clear()
            win.border(0)
            win.refresh()
            #buff.append("\n")
            break
        
        col = col+1
        #go to next row
        if col == 132:
            row = row+1
            col = 1
        

    return buff

def toWindow(window, message):
    if window.get_row() == 17:
        window.set_row(1)
        window.get_win().clear()
        window.get_win().border(0)
        window.get_win().refresh()
    window.get_win().addstr(window.get_row(), 1, message)
    window.add_row()
    window.get_win().border(0)
    window.get_win().refresh()
    
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
    lfound = False
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
            
    screen = curses.initscr()
    
    
        
    screen.border(0)
    curses.cbreak()
    curses.noecho()
    curses.nonl()
    a = 18
    b = 66
    c = 0
    d = 0
    
    
        
    try:
        box1 = curses.newwin(a, b, c+1, d+1)
        Win1 = window()
        Win1.set_win(box1)
        box2 = curses.newwin(a, b, c+1, b+1)
        Win2 = window()
        Win2.set_win(box2)
        box3 = curses.newwin(a, b, a+1, c+1)
        Win3 = window()
        Win3.set_win(box3)
        box4 = curses.newwin(a, b, a+1, b+1)
        Win4 = window()
        Win4.set_win(box4)
        box5 = curses.newwin(7, 132, 37, c+1)
        Win5 = window()
        Win5.set_win(box5)
        
        windows = [Win1, Win2, Win3, Win4, Win5]
        
        for box in windows:
            box.get_win().box()
            screen.refresh()
            box.get_win().refresh()
        running = 1
        listenlTrue = True
        listenrTrue = False
        while running:
            
                            
            if rfound == False:
                piggyr = 0
                rfound = True
                if ParamVars.get_noright() == False and ParamVars.get_raddr() != None:
                    
                #Create send connection
                    piggyr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    if int(ParamVars.get_useport()) != 36763:
                        piggyr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        try:
                            piggyr.bind((socket.gethostname(), int(ParamVars.get_useport())))
                            listenrTrue = False
                            piggyr.connect((ParamVars.get_raddr(), 36763))
                        except socket.error:
                            windows[4].get_win().addstr(1, 1, "already using this port\n")    
                            windows[4].get_win().refresh()
                    
                    

                input = [piggy, sys.stdin, piggyr]

            inputready, outputready, exceptready = select.select(input, [], [])
            for s in inputready:
                if s == piggy and piggy != 0 and listenlTrue:
                    client, address = piggy.accept()
                    
                    if ParamVars.get_lacctip() != None and ParamVars.get_lacctport() != None:
                        if ParamVars.get_lacctip() == address[0] and ParamVars.get_lacctport == address[1]:
                            input.append(client)
                    elif ParamVars.get_lacctip() != None and ParamVars.get_lacctport() == None:
                        if ParamVars.get_lacctip() == address[0]:
                            input.append(client)
                    elif ParamVars.get_lacctip() == None and ParamVars.get_lacctport() != None:
                        if ParamVars.getlacctport() == address[1]:
                            input.append(client)
                    else:
                        input.append(client)

                    
                elif s == piggyr and piggyr != 0 and listenrTrue:
                    client, address = piggyr.accept()
                    if ParamVars.get_racctip() != None and ParamVars.get_racctport() != None:
                        if ParamVars.get_racctip() == address[0] and ParamVars.get_racctport == address[1]:
                            input.append(client)
                    elif ParamVars.get_racctip() != None and ParamVars.get_racctport() == None:
                        if ParamVars.get_racctip() == address[0]:
                            input.append(client)
                    elif ParamVars.get_racctip() == None and ParamVars.get_racctport() != None:
                        if ParamVars.getracctport() == address[1]:
                            input.append(client)
                    else:
                        input.append(client)
                #Keyboard input
                elif s == sys.stdin:
                    message = ("".join(typed(windows[4]))).strip()
                    
                        
                    if message:
                        
                        #doCommand function returns True if message is a command, false otherwise
                        
                        
                        Commandval = ParamVars.doCommand(message)
                        if Commandval == True and Imode == False:
                            
                            if ParamVars.get_listenl() != None:
                                piggy.close()
                                input.remove(piggy)
                                piggy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                piggy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                try:
                                    piggy.bind(("", ParamVars.get_listenl()))
                                
                                    piggy.listen(5)
                                    listenlTrue = True
                                    input.append(piggy)
                                except socket.error:
                                    windows[4].get_win().addstr(1, 1, "already using this port\n")    
                                    windows[4].get_win().refresh()
                                ParamVars.set_listenl(None)
                                ParamVars.set_noleft(False)
                                
                            if ParamVars.get_listenr() != None:
                                piggyr.close()
                                input.remove(piggyr)
                                piggyr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                try:
                                    piggyr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                
                                    piggyr.bind(("", ParamVars.get_listenr()))
                                    piggyr.listen(5)
                                    intput.append(piggyr)
                                    listenrTrue = True
                                except socket.error:
                                    windows[4].get_win().addstr(1, 1, "already using this port\n")    
                                    windows[4].get_win().refresh()
                                ParamVars.set_listenr(None)
                                ParamVars.set_noright(False)
                                
                            
                            if ParamVars.get_connectrinput():
                        
                                
                                ParamVars.set_connectrinput(False)
                                piggyr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                if int(ParamVars.get_useport()) != 36763:
                                    piggyr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                    piggyr.bind((socket.gethostname(), int(ParamVars.get_useport())))
                                listenrTrue = False
                                piggyr.connect((ParamVars.get_raddr(), 36763))
                                
                                #input.remove(0)
                                input.append(piggyr)
                                
                            if ParamVars.get_connectlinput():
                        
                                
                                ParamVars.set_connectlinput(False)
                                piggyl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                if int(ParamVars.get_useport()) != 36763:
                                    piggyl.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                                    piggyl.bind((socket.gethostname(), int(ParamVars.get_useport())))
                                listenlTrue = False
                                piggyl.connect((ParamVars.get_laddr(), 36763))
                                lcon = piggyl
                                
                                input.append(piggyl)

                            if ParamVars.get_readFile() != None:
                                ParamVars.set_readFile(None)
                                filename = (message.split())[1]
                                file = open(filename, 'r')
                                text = file.read()
                                if ParamVars.get_outputl():
                                    toWindow(windows[2], text)
                                    sendLeft(text, lcon, windows[4])
                                if ParamVars.get_outputr():
                                    toWindow(windows[1], text)
                                    sendRight(text, piggyr, windows[4])
                                    
                                
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
                            if ParamVars.get_output() == True:
                                if ParamVars.get_outputl() == True:
                                    windows[4].get_win().addstr(1, 1, "output is to the left")
                                elif ParamVars.get_outputr() == True:
                                    windows[4].get_win().addstr(1, 1, "output is to the right")
                                else:
                                    windows[4].get_win().addstr(1, 1, "no output direction set")
                                
                                windows[4].get_win().refresh()
                                ParamVars.set_output(False)
                        elif Commandval != False:
                            windows[4].get_win().addstr(1, 1, str(Commandval))
                            windows[4].get_win().refresh()
                            
                                
                                
                                
                                
                            #Double command bug found
                            #message = sys.stdin.readline()
                        if message == "i" or Imode == True:
                            if Imode == False:
                                message = "".join(typed(windows[4]))
                            Imode = True

                            #if(not(ParamVars.IamHead())):
                            #   message = sys.stdin.readline()
                            if message.strip() == chr(27):
                                
                                Imode = False
                            else:
                                if(ParamVars.get_loopr() != True and ParamVars.get_loopl() != True):
                                    if ParamVars.get_outputr():
                                        if ParamVars.get_loopr():
                                            toWindow(windows[2], message.decode())
                                            sendLeft(message, lcon)
                                        else:
                                            toWindow(windows[1], message.decode())
                                            sendRight(message, piggyr, windows[4])
                                    if ParamVars.get_outputl(): 
                                        if ParamVars.get_loopl():
                                            toWindow(windows[1], message.decode())
                                            sendRight(message, piggyr, windows[4])
                                        else:
                                            toWindow(windows[2], message.decode())
                                            sendLeft(message, lcon, windows[4])
                
                #Recieve from right
                elif s == piggyr and piggyr != 0:
                    try:
                        message = s.recv(size)
                    except socket.error:
                        windows[4].get_win().addstr(1, 1, "Connection stopped from the right")
                        windows[4].get_win().refresh()
                    if message != '':
                        #if(ParamVars.get_dsprl()):
                        toWindow(windows[3], message.decode())
                            #print("Recieve from the right: %s" %message.decode())

                        #if(ParamVars.IamMiddle() or ParamVars.IamTail()):
                        #    if not(ParamVars.get_loopl() and ParamVars.get_loopr()):
                        if ParamVars.get_loopl():
                            toWindow(windows[1], message.decode())
                            sendRight(message, piggyr, windows[4])
                        elif not ParamVars.get_noleft():
                            toWindow(windows[2], message.decode())
                            sendLeft(message, lcon, windows[4])

                    else:
                        break
                #recieve from left
                elif s != 0:
                    lcon = s

                    if(ParamVars.checkladdr(s) or ParamVars.checkacctport(s)):
                        windows[4].get_win().addstr(1, 1,"Connection rejected")
                        windows[4].get_win().refresh()
                        s.close()
                        input.remove(s)
                        break
                    try:
                        data = s.recv(size)
                        if data == "":
                            s.close()
                            input.remove(s)
                    except socket.error:
                        windows[4].get_win().addstr(1, 1, "Connection stopped from the left\n")
                        windows[4].get_win().refresh()
                    if data:
                        #if(ParamVars.get_dsplr() == True):
                        toWindow(windows[0], data.decode())
                        
                            #print("From left side: %s" %data.decode())

                        if(ParamVars.IamHead() or ParamVars.IamMiddle()):
                            if data:
                                if(not(ParamVars.get_loopr() and ParamVars.get_loopl())):
                                    if ParamVars.get_loopr():
                                        toWindow(windows[2], data.decode())
                                        sendLeft(data, s)
                                    else:
                                        toWindow(windows[1], data.decode())
                                        sendRight(data, piggyr, windows[4])
                        elif ParamVars.get_loopr():
                            if data:
                                toWindow(windows[2], data.decode())
                                sendLeft(data, s, windows[4])
                        sys.stdout.flush()
        screen.getch()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()

if __name__=="__main__":
    main(sys.argv[1:])
