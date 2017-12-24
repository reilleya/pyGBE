from . import registers

def add(opA, opB):
    return opA + opB


func = {
        0x87 : [add, 'a', 'b'],
        0x80 : [add, 'a', 'b'],
        0x81 : [add, 'a', 'c'],
        0x82 : [add, 'a', 'd'],
        0x83 : [add, 'a', 'e'],
        0x84 : [add, 'a', 'h'],
        0x85 : [add, 'a', 'l']
      }

class core():
    def __init__(self):
        self.reg = registers.registers()
        
    def execute(self, inst):
        self.reg.dumpState()
        self.reg.setReg('A', 6)
        self.reg.dumpState()
        self.reg.setReg('C', 4)
        self.reg.dumpState()
        lookup = func[inst[0]]
        res = lookup[0](self.reg.getReg(lookup[1]), self.reg.getReg(lookup[2]))
        self.reg.setReg('a', res)
        self.reg.dumpState()
        
    
    
    
    def parseROM(self, rom):
        self.rom = []
        with open(rom,'rb') as file:
            cont = file.read()
            for c in cont:
                self.rom.append(hex(c))
        print(self.rom)