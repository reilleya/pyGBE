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
        self.LCDCEnabled = False
        self.timerEnabled = False
        self.serialCompEnabled = False
        self.edgeEnabled = False
        
    def update(self):
        pass
        
    def read(self, loc):
        if loc == 0xFFFF:
            return combineBits(self.vblankEnabled, self.LCDCEnabled, self.timerEnabled,
                                self.serialCompEnabled, self.edgeEnabled)
    
    def write(self, loc, value):
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
    
    def callInt(self, loc):
        self.enabled = False
        
        self.core.reg.setReg("sp", loc)