import pygame, threading

class display():
    def __init__(self, core):
        self.core = core
        
        self.ycoord = 0
        
        #Window stuff
        pygame.init()
        self.window = pygame.display.set_mode([160, 144])
        self.window.fill([255, 255, 255])
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exit")
        pygame.display.flip()
        
    def read(self, loc):
        if loc == 0xFF44:
            return self.ycoord
    
    def write(self, loc, value):
        pass