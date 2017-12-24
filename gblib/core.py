from . import registers
from . import functable as f

class core():
    def __init__(self):
        self.reg = registers.registers()
    
    def decodeAndExec(self, opc, index):
        print(str(hex(opc)) + " at " + str(index))
        if f[opc][0] == "add":
            res = self.reg.getReg(f[opc][1][0]) + self.reg.getReg(f[opc][1][1])
            self.reg.setBit('f', 'z', res == 0)
        #elif f[opc][0] == ""
        elif f[opc][0] == "nimp":
            print("OPCODE NOT IMPLEMENTED")
        else:
            print("OPCODE NOT FOUND")
        
        if f[opc][2] is not None:
            self.reg.setReg(f[opc][2], res)
    
    def parseROM(self, rom):
        self.rom = []
        with open(rom,'rb') as file:
            cont = file.read()
            for c in cont:
                self.rom.append(hex(c))
        #print(self.rom)