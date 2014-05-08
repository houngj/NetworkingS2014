import curses 

screen = curses.initscr()

try:
    
    screen.border(0)
    
    a = 18
    b = 66
    c = 0
    d = 0
    
    box1 = curses.newwin(a, b, c, d)
    box2 = curses.newwin(a, b, c, b)
    box3 = curses.newwin(a, b, a, c)
    box4 = curses.newwin(a, b, a, b)
    box5 = curses.newwin(7, 132, 36, c)
    
    windows = [box1, box2, box3, box4, box5]
    
    for box in windows:
        box.box()
        box.addch(5, 1, ord('a')+ 0)
        screen.refresh()
        box.refresh()
        
        
        screen.getch()
        
finally:
    curses.endwin()
        
