from . import registers

def add(opA, opB):
    return opA + opB

def sub(opA, opB):
    return opA - opB


#op : [func, [args, string=reg, num=reladdr], dest]
func = {
        0x87 : [add, ['a', 'b'], 'a'],
        0x80 : [add, ['a', 'b'], 'a'],
        0x81 : [add, ['a', 'c'], 'a'],
        0x82 : [add, ['a', 'd'], 'a'],
        0x83 : [add, ['a', 'e'], 'a'],
        0x84 : [add, ['a', 'h'], 'a'],
        0x85 : [add, ['a', 'l'], 'a']
      }

class core():
    def __init__(self):
        self.reg = registers.registers()
        
    def execute(self, inst):
        
        lookup = func[inst[0]]
        res = lookup[0](self.reg.getReg(lookup[1]), self.reg.getReg(lookup[2]))
        self.reg.setReg('a', res)
        self.reg.dumpState()
        
    
    def decode(self, opcode, index):
        print(str(opcode) + " at " + str(index))
        
        self.execute(self, decoded)
    
    def parseROM(self, rom):
        self.rom = []
        with open(rom,'rb') as file:
            cont = file.read()
            for c in cont:
                self.rom.append(hex(c))
        #print(self.rom)