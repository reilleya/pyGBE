class register16():
    def __init__(self, bank):
        self.bank = bank
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
        
    def getBit(self, bit, upper = True):
        return (self.value >> (bit + upper * self.upperShift)) & 1
        
    def setBit(self, bit, value, upper = True):
        if not upper:
            if type(bit) is str:
                if bit == 'z': bit = 7 
                elif bit == 'n': bit = 6
                elif bit == 'h': bit = 5
                elif bit == 'c': bit = 4
        bit += (upper * self.upperShift)
        cutout = ~(1 << bit) & 0xFFFF
        self.value = (self.value & cutout) | (value << bit)
        
    def dumpState(self, mode, label = None):
        length = 4 if mode == 'x' else 16
        st = format(self.value, mode).zfill(length)
        half = int(length / 2)
        self.bank.core.logger.log(label + ": " + st[:half] + " " + st[half:])

class registers():
    def __init__(self, core):
        self.core = core
        self.afReg = register16(self)
        self.bcReg = register16(self)
        self.deReg = register16(self)
        self.hlReg = register16(self)
        self.spReg = register16(self)
        self.pcReg = register16(self)
    
    def dumpState(self, mode = 'b'):
        self.core.logger.log("Reg State:")
        self.afReg.dumpState(mode, "af")
        self.bcReg.dumpState(mode, "bc")
        self.deReg.dumpState(mode, "de")
        self.hlReg.dumpState(mode, "hl")
        self.spReg.dumpState(mode, "sp")
        self.pcReg.dumpState(mode, "pc")
    
    def setReg(self, r, value):
        if r == 'a': self.afReg.setUpper(value)
        elif r == 'b': self.bcReg.setUpper(value)
        elif r == 'c': self.bcReg.setLower(value)
        elif r == 'd': self.deReg.setUpper(value)
        elif r == 'e': self.deReg.setLower(value)
        elif r == 'f': self.afReg.setLower(value)
        elif r == 'h': self.hlReg.setUpper(value)
        elif r == 'l': self.hlReg.setLower(value)
        elif r == 'af': self.afReg.setValue(value)
        elif r == 'bc': self.bcReg.setValue(value)
        elif r == 'de': self.deReg.setValue(value)
        elif r == 'hl': self.hlReg.setValue(value)
        elif r == 'sp': self.spReg.setValue(value)
        elif r == 'pc': self.pcReg.setValue(value)
        else:
            print("UNKNOWN REG")
        
    def getReg(self, r):
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
            
    def setBit(self, r, bit, value):
        if r == 'a': return self.afReg.setBit(bit, value, True)
        elif r == 'b': return self.bcReg.setBit(bit, value, True)
        elif r == 'c': return self.bcReg.setBit(bit, value, False)
        elif r == 'd': return self.deReg.setBit(bit, value, True)
        elif r == 'e': return self.deReg.setBit(bit, value, False)
        elif r == 'f': return self.afReg.setBit(bit, value, False)
        elif r == 'h': return self.bcReg.setBit(bit, value, True)
        elif r == 'l': return self.bcReg.setBit(bit, value, False)
        #elif r == 'HL'
        else:
            print("UNKNOWN REG")
        
    def getBit(self, r, bit):
        if r == 'a': return self.afReg.getBit(bit, True)
        elif r == 'b': return self.bcReg.getBit(bit, True)
        elif r == 'c': return self.bcReg.getBit(bit, False)
        elif r == 'd': return self.deReg.getBit(bit, True)
        elif r == 'e': return self.deReg.getBit(bit, False)
        elif r == 'f': return self.afReg.getBit(bit, False)
        elif r == 'h': return self.bcReg.getBit(bit, True)
        elif r == 'l': return self.bcReg.getBit(bit, False)
        #elif r == 'HL'
        else:
            print("UNKNOWN REG")
        