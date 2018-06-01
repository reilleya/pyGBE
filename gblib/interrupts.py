def combineBits(*args):
    out = 0
    for pos, arg in enumerate(args):
        out += (2**pos) * arg
    return out

class interrupts():
    def __init__(self, core):
        self.core = core
        self.enabled = True
        
        self.vblankEnabled = False
        self.vblankTrig = False
        
        self.LCDCEnabled = False
        self.LCDCTrig = False
        
        self.timerEnabled = False
        self.timerTrig = False
        
        self.serialCompEnabled = False
        self.serialCompTrig = False
        
        self.edgeEnabled = False
        self.edgeTrig = False
        
    def update(self):
        pass
        
    def read(self, loc):
        if loc == 0xFF0F:
            return combineBits(self.vblankTrig, self.LCDCTrig, self.timerTrig,
                                self.serialCompTrig, self.edgeTrig)
        
        if loc == 0xFFFF:
            return combineBits(self.vblankEnabled, self.LCDCEnabled, self.timerEnabled,
                                self.serialCompEnabled, self.edgeEnabled)
    
    def write(self, loc, value):
        if loc == 0xFF0F:
            self.vblankTrig = bool(value & 0b00001)
            self.LCDCTrig = bool(value & 0b00010)
            self.timerTrig = bool(value & 0b00100)
            self.serialCompTrig = bool(value & 0b01000)
            self.edgeTrig = bool(value & 0b10000)
    
        if loc == 0xFFFF:
            self.vblankEnabled = bool(value & 0b00001)
            self.LCDCEnabled = bool(value & 0b00010)
            self.timerEnabled = bool(value & 0b00100)
            self.serialCompEnabled = bool(value & 0b01000)
            self.edgeEnabled = bool(value & 0b10000)
        
    def enable(self):   # TODO: Delayed enabling
        self.enabled = True
    
    def disable(self):
        self.enabled = False
        
    def trigger(self, type):
        if self.enabled:
            jmpAddr = None
            if type == 2: # Timer
                if self.timerEnabled:
                    self.timerTrig = True
                    jmpAddr = 0x0050
                    
            if jmpAddr is not None:
                self.enabled = False
                self.core.push(self.core.reg.getReg("sp"))
                self.core.reg.setReg("sp", jmpAddr)