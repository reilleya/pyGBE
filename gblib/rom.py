class ROMException(Exception):
    """Raise for any error associated with system memory"""

class rom():
    def __init__(self, romdata):
        self.romData = romdata
        self.romType = None
        self.mode = 0
        self.detectType()
        
    def detectType(self):
        #print("Booting " + self.getName())
        #print("ROM type: " + str(self.romData[0x147]))
        self.romType = self.romData[0x147]
        if self.romType == 0:
            pass
            #print("ROM only detected")
        elif self.romType == 1:
            self.mode = 0
            #print("MCB1")
        else:
            raise ROMException("Unsupported ROM type #"+str(self.romType))
    
    def write(self, loc, value):
        if self.romType == 0:
            #raise ROMException("ROM type 0 does not support writes") Annoyingly, some games do this anyway
            print("Warning, ROM only cartridges do not support writes")
            
        elif self.romType == 1:
            if loc >= 0x6000 and loc <= 0x7FFF:
                self.mode = loc & 0x1
    
    def read(self, loc):
        if self.romType == 0:
            return self.romData[loc]
        if self.romType == 1:
            return self.romData[loc] # TODO: Implement bank switching
            
    def getName(self):
        name = ""
        for i in range(0x134, 0x143):
            name += chr(self.romData[i])
        return name