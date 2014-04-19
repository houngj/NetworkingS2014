import argparse, socket

class Param:
    def __init__(self):
        self.acctport = ""
        self.useport = 36763
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
            
        if (s.getpeername()[0] != self.laddr and self.laddr != None):
            return True
        else:
            return False
        
        
    def checkacctport(self, s):
        if(s.getpeername()[1] is self.acctport and self.acctport != ""):
            return True
        else:
            return False
    
    def Error(self):
        if(self.laddr == None and self.raddr == None and self.noright == False) or (self.noleft == True and self.noright == True):
            return True
        else:
            return False
        
        
    
    

    
