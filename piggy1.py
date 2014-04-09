import select, socket, sys, getopt, collections
import argparse

acctport = None
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
        noright = True;
        raddr = None;
    #if -noleft was raised in commandline, -laddr option is to be ignored    
    if(parser.noleft == True):
        noleft = True;
        laddr = None;
 
    if(parser.lacctport != None):
        if(parser.lacctport != "*"):
            lacctport = parser.lacctport
        else:
            allacctport = True
    
    if(parser.luseport != None):
        if(parser.luseport != "*"):
            useport = parser.luseport
            alluseport = False
        else:
            alluseport = True




def main(argv):
    
    parser = Commandline_Param(argv)
    EvalParam(parser)
    
    test()
    
    

if __name__=="__main__":
    main(sys.argv[1:])
