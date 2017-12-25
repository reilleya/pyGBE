from . import registers
from . import functable as f

class core():
    def __init__(self):
        self.reg = registers.registers()
        self.memory = []
    
    def decodeAndExec(self, opc, index):
        print(str(hex(opc)) + " at " + str(index))
        if f[opc][0] == "add":
            res = self.reg.getReg(f[opc][1][0]) + self.reg.getReg(f[opc][1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            if len(f[opc][2]) == 2:
                h1 = self.reg.getReg(f[opc][1][0]) >> 8
                h2 = self.reg.getReg(f[opc][1][1]) >> 8
                self.reg.setBit('f', 'h', (h1 & 0xF) + (h2 & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(f[opc][1][0]) + self.reg.getReg(f[opc][1][1]) & 0x10000)
            else:
                self.reg.setBit('f', 'h', (self.reg.getReg(f[opc][1][0]) & 0xF) + (self.reg.getReg(f[opc][1][1]) & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(f[opc][1][0]) + self.reg.getReg(f[opc][1][1]) & 0x100)
            
        elif f[opc][0] == "addcn": #Add a constant, for E8
            add = self.getMem(index + f[opc][1][1])
            res = self.reg.getReg(f[opc][1][0]) + add
            self.reg.setBit('f', 'z', False)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', (self.reg.getReg(f[opc][1][0]) & 0xF) + add > 0xF)
            self.reg.setBit('f', 'c', (self.reg.getReg(f[opc][1][0]) + add) & 0x10000)
            
        elif f[opc][0] == "addcr": #Addition with carry
            res = self.reg.getReg(f[opc][1][0]) + self.reg.getReg(f[opc][1][1]) + self.reg.getBit('f', 'c')
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            if len(f[opc][2]) == 2:
                h1 = self.reg.getReg(f[opc][1][0]) >> 8
                h2 = self.reg.getReg(f[opc][1][1]) + self.reg.getBit('f', 'c') >> 8
                self.reg.setBit('f', 'h', (h1 & 0xF) + (h2 & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(f[opc][1][0]) + self.reg.getReg(f[opc][1][1])  + self.reg.getBit('f', 'c') & 0x10000)
            else:
                self.reg.setBit('f', 'h', (self.reg.getReg(f[opc][1][0]) & 0xF) + (self.reg.getReg(f[opc][1][1]) & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(f[opc][1][0]) + self.reg.getReg(f[opc][1][1])  + self.reg.getBit('f', 'c') & 0x100)
            
        elif f[opc][0] == "sub":
            res = self.reg.getReg(f[opc][1][0]) - self.reg.getReg(f[opc][1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', not (self.reg.getReg(f[opc][1][0]) & 0x0F) < (self.reg.getReg(f[opc][1][1]) & 0x0F))
            self.reg.setBit('f', 'c', not self.reg.getReg(f[opc][1][0]) < self.reg.getReg(f[opc][1][1]))
            
        elif f[opc][0] == "sbc":
            res = self.reg.getReg(f[opc][1][0]) - (self.reg.getReg(f[opc][1][1]) - self.reg.getBit('f', 'c'))
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', not (self.reg.getReg(f[opc][1][0]) & 0x0F) < (self.reg.getReg(f[opc][1][1]) - self.reg.getBit('f', 'c') & 0x0F))
            self.reg.setBit('f', 'c', not self.reg.getReg(f[opc][1][0]) < self.reg.getReg(f[opc][1][1]) - self.reg.getBit('f', 'c'))
        
        elif f[opc][0] == "and":
            res = self.reg.getReg(f[opc][1][0]) & self.reg.getReg(f[opc][1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', True)
            self.reg.setBit('f', 'c', False)
            
        elif f[opc][0] == "or":
            res = self.reg.getReg(f[opc][1][0]) | self.reg.getReg(f[opc][1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', False)
            self.reg.setBit('f', 'c', False)
            
        elif f[opc][0] == "xor":
            res = self.reg.getReg(f[opc][1][0]) ^ self.reg.getReg(f[opc][1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', False)
            self.reg.setBit('f', 'c', False)
            
        elif f[opc][0] == "inc":
            res = self.reg.getReg(f[opc][1][0]) + 1
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', (self.reg.getReg(f[opc][1][0]) & 0xF) + 1 > 0xF)
        
        elif f[opc][0] == "inc16": #Needed for 16 bit incs because flags aren't updated?
            res = self.reg.getReg(f[opc][1][0]) + 1
            
        elif f[opc][0] == "dec16": #Same as inc16
            res = self.reg.getReg(f[opc][1][0]) - 1
        
        elif f[opc][0] == "dec":
            res = self.reg.getReg(f[opc][1][0]) - 1
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', not (self.reg.getReg(f[opc][1][0]) & 0x0F) < 1 & 0x0F)
        
        elif f[opc][0] == "loadcn":
            res = self.getMem(index + f[opc][1][0])
        
        elif f[opc][0] == "loadcn16":
            res = self.getMem(index + f[opc][1][0]) + (self.getMem(index + f[opc][1][1]) << 8)
        
        elif f[opc][0] == "mov":
            res = self.reg.getReg(f[opc][1][0])
        
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
    
    def getMem(self, index):
        return self.memory[index]