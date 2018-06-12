class logger():
    def __init__(self, toConsole = False, logFile = None):
        self.toConsole = toConsole
        if logFile is not None:
            self.logFile = open(logFile)
        else:
            self.logFile = None
    
    def log(self, message):
        if self.toConsole:
            print(message)
        if self.logFile is not None:
            self.logFile.write(message)
