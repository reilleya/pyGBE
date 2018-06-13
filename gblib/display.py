import pygame

class sprite():
    def __init__(self, display):
        self.display = display
        self.patternNum = 0
        self.x = 0
        self.y = 0
        self.priority = False
        self.yFlip = False
        self.xFlip = False
        self.palNum = False
        self.image = pygame.surface.Surface((8, 8))
        
    def draw(self):
        if self.display.largeSprites:
            size = (8, 16)
            data = self.display.getPattern(True, self.patternNum) + self.display.getPattern(True, self.patternNum + 1)
        else:
            size = (8, 8)
            data = self.display.getPattern(True, self.patternNum)
        self.image = pygame.surface.Surface(size)
        self.image.fill((255, 255, 255))

        for y in range(0, size[1]):
            for x in range(0, 8):
                idx = 2 ** (7 - x)
                if (data[y * 2] & idx) & (data[(y * 2) + 1] & idx):
                    self.image.set_at((x, y), (0, 0, 0))
                elif (data[y * 2] & idx):
                    self.image.set_at((x, y), (85, 85, 85))
                elif (data[(y * 2) + 1] & idx):
                    self.image.set_at((x, y), (170, 170, 170))
        
    def setPatternNum(self, pNum):
        self.patternNum = pNum
        self.draw()
    
    def write(self, loc, value):
        if loc == 0:
            self.y = value
        elif loc == 1:
            self.x = value
        elif loc == 2:
            self.patternNum = value
        elif loc == 3:
            self.priority = bool(value & 2**7)
            self.yFlip = bool(value & 2**6)
            self.xFlip = bool(value & 2**5)
            self.palNum = bool(value & 2**4)
        self.draw()
    
    def read(self, loc):
        if loc == 0:
            return self.y
        elif loc == 1:
            return self.x
        elif loc == 2:
            return self.patternNum
        elif loc == 3:
            return (self.priority * 2**7) + (self.yFlip * 2**6) + (self.xFlip * 2**5) + (self.palNum * 2**5)

class display():
    def __init__(self, core, openWindow = False):
        self.core = core
        
        self.ycoord = 0
        
        self.scroll = [0, 0]
        
        self.vblank = False
        self.lastLY = 0
        
        self.vram = [0]*0x2000
        self.oam = []
        
        self.sprites = []
        for i in range(0, 40):
            self.sprites.append(sprite(self))
        
        self.largeSprites = False #False for 8x8, True for 8x16
        
        #Window stuff
        self.openWindow = openWindow
        if self.openWindow:
            pygame.init()
            self.window = pygame.display.set_mode([160, 288])
            self.window.fill([255, 255, 255])
        
    def update(self):
        self.core.logger.log(self.core.clock.cycles)
        if self.core.clock.cycles - self.lastLY >= 456:
            self.lastLY = self.core.clock.cycles
            self.core.logger.log("LY!")
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
    
    def getPattern(self, sprite, number):
        if sprite:
            return self.vram[number * 16 : (number + 1) * 16]
        
    def read(self, loc):
        if loc == 0xFF40:
            return 0
        elif loc == 0xFF42:
            return self.scroll[1]
        elif loc == 0xFF43:
            return self.scroll[0]
        elif loc == 0xFF44:
            return self.ycoord
        self.core.logger.log("Disp read from " + str(hex(loc)))
    
    def write(self, loc, value):
        if loc >= 0x8000 and loc < 0xA000:
            self.vram[loc - 0x8000] = value
            
            if self.openWindow:
                self.window.fill([200, 255, 255])
                for x in range(0, 40):
                    self.sprites[x].draw()
                    self.window.blit(self.sprites[x].image, (x*8, 144))
                pygame.display.flip()
            
        elif loc < 0xFEA0:
            self.sprites[int((loc - 0xFE00)/ 4)].write(loc % 4, value)
            if self.openWindow:
                self.window.fill([200, 255, 255])
                for s in self.sprites:
                    s.draw()
                    self.window.blit(s.image, (s.x - 8, s.y - 16))
                pygame.display.flip()
        elif loc == 0xFF42:
            self.scroll[1] = value
        elif loc == 0xFF43:
            self.scroll[0] = value
        elif loc == 0xFF44:
            self.ycoord = 0
        elif loc == 0xFF46:
            print("OAM AT " + str(hex(value)))
        else:
            self.core.logger.log("Disp write to " + str(hex(loc)) + ", " + str(hex(value)))