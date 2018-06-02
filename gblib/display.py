import pygame, threading

class display():
    def __init__(self, core, openWindow = False):
        self.core = core
        
        self.ycoord = 0
        
        self.vblank = False
        
        #Window stuff
        self.openWindow = openWindow
        if self.openWindow:
            pygame.init()
            self.window = pygame.display.set_mode([160, 144])
            self.window.fill([255, 255, 255])
        
    def update(self):
        if self.core.clock.cycles % 456 == 0:
            print("LY!")
            self.ycoord += 1
            if self.ycoord == 144:
                print("VBLANK")
            if self.ycoord == 155:
                self.ycoord = 0
                
        
        
        if self.openWindow:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("exit")
            pygame.display.flip()
        
    def read(self, loc):
        if loc == 0xFF44:
            return self.ycoord
    
    def write(self, loc, value):
        if loc == 0xFF44:
            self.ycoord = 0