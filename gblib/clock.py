class clock():
    def __init__(self, core):
        self.core = core
        self.cycles = 0
        
        self.divReg = 0
        
        self.timerEnabled = False
        self.timerVal = 0
        self.timerResetVal = 0
        self.timerRate = 1024
        
    def reset(self):
        self.cycles = 0
        
    def stepCycles(self, cycles):
        self.cycles += cycles
        
        if cycles % 256 == 0:
            self.divReg += 1
            if self.divReg > 0xFF:
                self.divReg = 0
        
        if self.timerEnabled:
            if self.cycles % self.timerRate == 0:
                self.timerVal += 1
            if self.timerVal > 0xFF:
                self.timerVal = self.timerResetVal
                self.core.int.trigger(2) # Trigger a timer interrupt
        
    def read(self, loc):
        if loc == 0xFF04:
            return self.divReg
            
        if loc == 0xFF05:
            return self.timerVal
    
        if loc == 0xFF06: # Timer modulo
            return self.timerResetVal
        
    def write(self, loc, value):
        if loc == 0xFF04:
            self.divReg = 0
    
        if loc == 0xFF05:
            self.timerVal = value
    
        if loc == 0xFF06: # Timer modulo
            self.timerResetVal = value
        
        if loc == 0xFF07: # Timer control register
            self.timerEnabled = value & 0b100
            if value % 0b11 == 0:
                self.timerRate = 1024
            elif value % 0b11 == 1:
                self.timerRate = 16
            elif value % 0b11 == 2:
                self.timerRate = 64
            else:
                self.timerRate = 256
        
    @property
    def time(self):
        return self.cycles / (4.194304 * 10 ** 6)
        
    def __repr__(self):
        return "Cycles: " + str(self.cycles) + "\nTime: " + str(self.time)