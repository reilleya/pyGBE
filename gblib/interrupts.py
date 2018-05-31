class interrupts():
    def __init__(self, core):
        self.core = core
        self.enabled = True
        
    def update(self):
        pass
        
    def read(self, loc):
        return 0
        
    def enable(self):   # TODO: Delayed enabling
        self.enabled = True
    
    def disable(self):
        self.enabled = False