import pygame, threading

class display():
    def __init__(self, core, openWindow = False):
        self.core = core
        
        self.ycoord = 0
        
        self.scroll = [0, 0]
        
        self.vblank = False
        
        #Window stuff
        self.openWindow = openWindow
        if self.openWindow:
            pygame.init()
            self.window = pygame.display.set_mode([160, 144])
            self.window.fill([255, 255, 255])
        
    def update(self):
        if self.core.clock.cycles % 456 == 0:
            #print("LY!")
            self.ycoord += 1
            if self.ycoord == 144:
                pass
                #print("VBLANK")
            if self.ycoord == 155:
                self.ycoord = 0
                
        
        
        if self.openWindow:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("exit")
            pygame.display.flip()
        
    def read(self, loc):
        if loc == 0xFF42:
            return self.scroll[1]
        elif loc == 0xFF43:
            return self.scroll[0]
        elif loc == 0xFF44:
            return self.ycoord
        print("Disp read from " + str(hex(loc)))
    
    def write(self, loc, value):
        if loc == 0xFF42:
            self.scroll[1] = value
        elif loc == 0xFF43:
            self.scroll[0] = value
        elif loc == 0xFF44:
            self.ycoord = 0
        else:
            print("Disp write to " + str(hex(loc)) + ", " + str(hex(value)))