class register16():
    def __init__(self):
        self.value = 0
        self.upperMask = 65280
        self.upperShift = 8
        self.lowerMask = 255
        self.fullMask = 65535
        
    def getLower(self):
        return self.value & self.lowerMask
    
    def setLower(self, value):
        self.value = (self.value & self.upperMask) | (value & self.lowerMask)
        
    def getUpper(self):
        return (self.value & self.upperMask) >> self.upperShift
        
    def setUpper(self, value):
        self.value = (self.value & self.lowerMask) | ((value & self.lowerMask) << self.upperShift)
        
    def getValue(self):
        return self.value
        
    def setValue(self, value):
        self.value = value & self.fullMask
        
    def dumpState(self, mode, label = None):
        length = 4 if mode == 'x' else 16
        st = format(self.value, mode).zfill(length)
        half = int(length / 2)
        print(label + ": " + st[:half] + " " + st[half:])

class registers():
    def __init__(self):
        self.afReg = register16()
        self.bcReg = register16()
        self.deReg = register16()
        self.hlReg = register16()
        self.spReg = register16()
        self.pcReg = register16()
    
    def dumpState(self, mode = 'b'):
        print("Reg State:")
        self.afReg.dumpState(mode, "AF")
        self.bcReg.dumpState(mode, "BC")
        self.deReg.dumpState(mode, "DE")
        self.hlReg.dumpState(mode, "HL")
        self.spReg.dumpState(mode, "SP")
        self.pcReg.dumpState(mode, "PC")
    
    def setReg(self, reg, value):
        r = reg.lower()
        if r == 'a': return self.afReg.setUpper(value)
        elif r == 'b': return self.bcReg.setUpper(value)
        elif r == 'c': return self.bcReg.setLower(value)
        elif r == 'd': return self.deReg.setUpper(value)
        elif r == 'e': return self.deReg.setLower(value)
        elif r == 'f': return self.afReg.setLower(value)
        elif r == 'h': return self.hlReg.setUpper(value)
        elif r == 'l': return self.hlReg.setLower(value)
        elif r == 'af': return self.afReg.setValue(value)
        elif r == 'bc': return self.bcReg.setValue(value)
        elif r == 'de': return self.deReg.setValue(value)
        elif r == 'hl': return self.hlReg.setValue(value)
        elif r == 'sp': return self.spReg.setValue(value)
        elif r == 'pc':return self.pcReg.setValue(value)
        else:
            print("UNKNOWN REG")
        
    def getReg(self, reg):
        r = reg.lower()
        if r == 'a': return self.afReg.getUpper()
        elif r == 'b': return self.bcReg.getUpper()
        elif r == 'c': return self.bcReg.getLower()
        elif r == 'd': return self.deReg.getUpper()
        elif r == 'e': return self.deReg.getLower()
        elif r == 'f': return self.afReg.getLower()
        elif r == 'h': return self.hlReg.getUpper()
        elif r == 'l': return self.hlReg.getLower()
        elif r == 'af': return self.afReg.getValue()
        elif r == 'bc': return self.bcReg.getValue()
        elif r == 'de': return self.deReg.getValue()
        elif r == 'hl': return self.hlReg.getValue()
        elif r == 'sp': return self.spReg.getValue()
        elif r == 'pc':return self.pcReg.getValue()
        else:
            print("UNKNOWN REG")