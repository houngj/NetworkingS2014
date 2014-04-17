import argparse

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
        loopl - %s\n""" %(self.acctport, self.useport, self.laddr, self.raddr, self.noleft, self.noright, self.dsplr, self.dsprl, self.loopr, self.loopl))
        



    def EvalParam(self, parser):
        if(parser.laddr != None):
            if(parser.laddr != "*"):
                self.laddr = parser.laddr
                
                
        if(parser.raddr != None):
            if(parser.raddr != "*"):
                self.raddr = parser.raddr
            
        #if -noright was raised in commandline, -raddr option is to be ignored
        if(parser.noright == True):
            self.noright = True
            self.raddr = None
        #if -noleft was raised in commandline, -laddr option is to be ignored    
        if(parser.noleft == True):
            self.noleft = True
            self.laddr = None
 
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
    
    
    

    