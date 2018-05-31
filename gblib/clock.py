class clock():
    def __init__(self, core):
        self.core = core
        self.cycles = 0
        
    def reset(self):
        self.cycles = 0
        
    def stepCycles(self, cycles):
        self.cycles += cycles
        # Check timers
        
    def read(self, loc):
        return 0
        
    def write(self, loc, value):
        pass
        
    @property
    def time(self):
        return self.cycles / (4.194304 * 10 ** 6)
        
    def __repr__(self):
        return "Cycles: " + str(self.cycles) + "\nTime: " + str(self.time)