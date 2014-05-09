import argparse, socket, sys





class Param:
    def __init__(self):
        self.acctport = ""
        self.useport = 36763
        self.luseport = 36763
        self.laddr = None
        self.raddr = None
        self.noleft = False
        self.noright = False
        self.dsplr = False
        self.dsprl = False
        self.loopr = False
        self.loopl = False
        self.outputl = False
        self.outputr = True
        self.output = False
        self.connectrinput = False
        self.connectlinput = False
        self.readFile = None
        self.listenr = None
        self.listenl = None
        self.lacctip = None
        self.racctip = None
        self.lacctport = None
        self.racctport = None

    def get_racctport(self):
        return self.racctport

    def get_lacctport(self):
        return self.lacctport
    def get_lacctip(self):
        return self.lacctip
    def get_racctip(self):
        return self.racctip
    def get_outputl(self):
        return self.outputl
    def get_outputr(self):
        return self.outputr
    def get_noleft(self):
        return self.noleft
    def get_acctport(self):
        return self.acctport
    def get_useport(self):
        return self.useport
    def get_laddr(self):
        return self.laddr
    def get_raddr(self):
        return self.raddr
    def get_noright(self):
        return self.noright
    def get_dsplr(self):
        return self.dsplr
    def get_dsprl(self):
        return self.dsprl
    def get_loopr(self):
        return self.loopr
    def get_loopl(self):
        return self.loopl
    def get_output(self):
        return self.output
    def get_connectrinput(self):
        return self.connectrinput
    def get_connectlinput(self):
        return self.connectlinput
    def get_readFile(self):
        return self.readFile
    def get_listenl(self):
        return self.listenl
    def get_listenr(self):
        return self.listenr

        
    def set_outputl(self, Val):
        self.outputl = Val
    def set_outputr(self, Val):
        self.outputr = Val
    def set_dsplr(self, Val):
        self.dsplr = Val
    def set_dsprl(self, Val):
        self.dsprl = Val
    def set_noright(self, Val):
        self.noright = Val
    def set_noleft(self, Val):
        self.noleft = Val
    def set_output(self, Val):
        self.output = Val
    def set_connectrinput(self, Val):
        self.connectrinput = Val
    def set_connectlinput(self, Val):
        self.connectlinput = Val
    def set_readFile(self, Val):
        self.readFile = Val
    def set_listenl(self, Val):
        self.listenl = Val
    def set_listenr(self, Val):
        self.listenr = Val
    
    def Commandline_Param(self,argv):
        parser = argparse.ArgumentParser(description="Parse commandline parameters")
        
        parser.add_argument("-laddr", action='store', dest='laddr')
        parser.add_argument("-raddr", action='store', dest='raddr')
        parser.add_argument("-noleft", action='store_true', dest='noleft')
        parser.add_argument("-noright", action='store_true', dest='noright')
        parser.add_argument("-lacctport", action='store', dest='lacctport')
        parser.add_argument("-luseport", action='store', dest='luseport')
        parser.add_argument("-dsplr", action='store_true', dest='dsplr')
        parser.add_argument("-dsprl", action='store_true', dest='dsprl')
        parser.add_argument("-loopr", action='store_true', dest='loopr')
        parser.add_argument("-loopl", action='store_true', dest='loopl')
        
        string = " ".join(argv)
        return parser.parse_args(string.split())
    
    
    
    def test(self):
        print("""acctport - %s\n        
        useport - %s\n        
        laddr - %s\n
        raddr - %s\n
        noleft - %s\n
        noright - %s\n
        dsplr - %s\n
        dsprl - %s\n
        loopr - %s\n
        loopl - %s\n
        outputr - %s\n
        outputl - %s\n""" %(self.acctport, self.useport, self.laddr, self.raddr, self.noleft, self.noright, self.dsplr, self.dsprl, self.loopr, self.loopl, self.outputr, self.outputl))
        



    def EvalParam(self, parser):
        if(parser.laddr != None):
            if(parser.laddr != "*"):
                self.laddr = socket.gethostbyname(parser.laddr)
                
                
        if(parser.raddr != None):
            if(parser.raddr != "*"):
                self.raddr = socket.gethostbyname(parser.raddr)
            
        
 
        if(parser.lacctport != None):
            if(parser.lacctport != "*"):
                self.acctport = parser.lacctport
    
        if(parser.luseport != None):
            if(parser.luseport != "*"):
                self.useport = parser.luseport
                
        if (parser.dsplr == True) or (parser.dsplr == False and parser.dsprl == False):
            self.dsplr = True
        if (parser.dsprl == True):
            self.dsprl = True
        if(parser.dsplr == True and parser.dsprl == True):
            self.dsplr = True
            self.dsprl = False
        
        if(parser.loopr == True):
            self.loopr = True
        if(parser.loopl == True):
            self.loopl = True
        
        #if -noright was raised in commandline, -raddr option is to be ignored, direction parameters ignored, output to left
        if(parser.noright == True):
            self.noright = True
            self.raddr = None
            self.dsprl = False
            self.dsplr = True
            self.outputl = True
            self.outputr = False
        #if -noleft was raised in commandline, -laddr option is to be ignored, direction parameters ignored    
        if(parser.noleft == True):
            self.noleft = True
            self.laddr = None
            self.dsprl = True
            self.dsplr = False
            
            
            
    def checkladdr(self, s):
        try:
            if (s.getpeername()[0] != self.laddr and self.laddr != None):
                return True
            else:
                return False
        except socket.error:
            None
        
        
    def checkacctport(self, s):
        try:
            if(s.getpeername()[1] is self.acctport and self.acctport != ""):
                return True
            else:
                return False
        except socket.error:
            None
    
    def Error(self):
        if(self.laddr == None and self.raddr == None and self.noright == False) or (self.noleft == True and self.noright == True):
            return True
        else:
            return False
        
    def IamHead(self):
        if(self.noright == False and self.noleft == True):
            return True
        else:
            return False

    def IamTail(self):
        if(self.noright == True and self.noleft == False):
            return True
        else:
            return False
            
    def IamMiddle(self):
        if(self.noright == False and self.noleft == False):
            return True
        else:
            return False
    
    
    def doCommand(self, message):
        splitmessage = message.split()
        message = splitmessage[0]
        if message == ":outputl":
            if self.IamHead() == True:
                print("No connection to the left\n")
            else:
                self.outputl = True
                self.outputr = False
            return True
        elif message == ":outputr":
            if self.IamTail() == True:
                print("No connection to the right\n")
            else:
                self.outputr = True
                self.outputl = False
            return True
        elif message == ":dsplr":
            self.dsplr = True
            self.dsprl = False
            return True
        elif message == ":dsprl":
            self.dsplr = False
            self.dsprl = True
            return True
        elif message == ":noright":
            self.noright = True
            return True
        elif message == ":noleft":
            self.noleft = True
            return True
        elif message == ":loopr":
            
            self.loopr = True
            return True
        elif message == ":loopl":
            self.loopl = True
            return True
        elif message == ":q":
            sys.exit()
            return True
        elif message == ":output":
            self.output = True
            return True
        elif message == ":connectr":
            try:
                self.noright = False
                self.connectrinput = True
                self.raddr = socket.gethostbyname(splitmessage[1])
                self.useport = int(splitmessage[2])
                return True
            except:
                return "Impropper IP or Port; Usage: ':connectr IP Port'"
        elif message == ":connectl":
            try:
                self.noleft = False
                self.connectlinput = True
                self.laddr = socket.gethostbyname(splitmessage[1])
                self.useport = int(splitmessage[2])
                return True
            except:
                return "Impropper IP or Port; Usage: ':connectl IP Port'"
        elif message == ":listenl":
            if len(splitmessage) > 1:
                self.listenl = splitmessage[1]
            else:
                self.listenl = 36763
            return True
        elif message ==":listenr":
            if len(splitmessage) > 1:
                self.listenr = splitmessage[1]
            else:
                self.listenr = 36763
            return True
        elif message ==":read":
            self.readFile = splitmessage[1]
            return True
        elif message ==":luseport":
            try:
                self.luseport = splitmessage[1]
                return True
            except:
                return "improper Port; Usage: ':luseport Port'"
        elif message ==":ruseport":
            try:
                self.useport = splitmessage[1]
                return True
            except:
                return "improper Port; Usage: ':ruseport Port'"
            None
        elif message == ":lacctport":
            
            try:
                self.lacctrport = splitmessage[1]
                return True
            except:
                return "improper Port; Usage: ':lacctport Port'"
            
        elif message == ":racctport":
            
            try:
                self.lracctrport = splitmessage[1]
                return True
            except:
                return "improper Port; Usage: ':racctport Port'"
            
        elif message == ":lacctip":
            try:
                self.lacctrip = splitmessage[1]
                return True
            except:
                return "improper IP; Usage: ':lacctip IP'"
        elif message == ":racctip":
            try:
                self.racctrip = splitmessage[1]
                return True
            except:
                return "improper IP; Usage: ':racctip IP'"
            
        else:
            return False

    
