from . import registers
from . import functable as f

def tc(num):
    return num - (256 * bool(num & 0x80))

class core():
    def __init__(self):
        self.reg = registers.registers()
        self.rom = []
        
        self.totalCycles = 0
        self.interruptsEnabled = True
    
    def loop(self):
        ind = self.reg.getReg('pc')
        op = self.getMem(ind)
        #print('Running ' + str(hex(op)) + ' at ' + hex(ind))
        self.decodeAndExec(op, ind)
        self.checkInterrupts()
    
    def decodeAndExec(self, opc, index):
        step = True
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
            if type(f[opc][1][1]) is int:
                sv = self.getMem(index + f[opc][1][1])
            else:
                sv = self.reg.getReg(f[opc][1][1])
            res = self.reg.getReg(f[opc][1][0]) - sv
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', (self.reg.getReg(f[opc][1][0]) & 0x0F) < sv & 0x0F)
            self.reg.setBit('f', 'c', self.reg.getReg(f[opc][1][0]) < sv)
            
        elif f[opc][0] == "sbc":
            res = self.reg.getReg(f[opc][1][0]) - (self.reg.getReg(f[opc][1][1]) - self.reg.getBit('f', 'c'))
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', (self.reg.getReg(f[opc][1][0]) & 0x0F) < (self.reg.getReg(f[opc][1][1]) - self.reg.getBit('f', 'c') & 0x0F))
            self.reg.setBit('f', 'c', self.reg.getReg(f[opc][1][0]) < self.reg.getReg(f[opc][1][1]) - self.reg.getBit('f', 'c'))
        
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
        
        elif f[opc][0] == "jump":
            self.reg.setReg('pc', (self.getMem(index + f[opc][1][0]) << 8) + self.getMem(index + f[opc][1][1]))
            step = False
            
        elif f[opc][0] == "jumpR":
            if (self.reg.getReg('f') & f[opc][1][0]) == f[opc][1][1]:
                #step = False <- maybe not?
                jump = tc(self.getMem(index + f[opc][1][2]))
                self.reg.setReg('pc', self.reg.getReg('pc') + jump)
        
        elif f[opc][0] == "disInt":
            self.interruptsEnabled = False # This is probably wrong
            
        elif f[opc][0] == "saveMem":
            offset = self.getMem(index + f[opc][1][2])
            self.setMem(f[opc][1][1] + offset, self.reg.getReg(f[opc][1][0]))
        
        elif f[opc][0] == "loadMem":
            offset = self.getMem(index + f[opc][1][1])
            res = self.getMem(f[opc][1][0] + offset)
            
        elif f[opc][0] == "push16":
            val = self.reg.getReg(f[opc][1][0])
            loc = self.reg.getReg("sp")
            self.setMem(loc - 1, val & 0x00FF)
            self.setMem(loc - 2, (val & 0xFF00) >> 8)
            res = loc - 2
        
        elif f[opc][0] == "pop16":
            loc = self.reg.getReg("sp")
            v = [self.getMem(loc), self.getMem(loc + 1)]
            print(v)
            res = (v[1] + (v[0] << 8))
            self.reg.setReg("sp", loc + 2)

        elif f[opc][0] == "nop":
            pass
        
        elif f[opc][0] == "nimp":
            raise NameError("OP " + str(hex(opc)) + " not implemented!")
            
        else:
            raise NameError("Opcode not found")
        
        if f[opc][2] is not None:
            self.reg.setReg(f[opc][2], res)

        if step:
            self.reg.setReg('pc', self.reg.getReg('pc') + f[opc][3])
            
        self.totalCycles += f[opc][4]
    
    def parseROM(self, rom):
        with open(rom,'rb') as file:
            cont = file.read()
            for c in cont:
                self.rom.append(int(c))
        #print(self.rom)
    
    def getMem(self, index):
        #print("Loading " + str(index))
        return self.rom[index]
        
    def setMem(self, index, value):
        #print("Saving " + str(hex(value)) + " to " + str(hex(index)))
        self.rom[index] = value
    
    def checkInterrupts(self):
        if self.interruptsEnabled:
            intf = self.getMem(0xFF0F) & self.getMem(0xFFFF)
            if intf & 0x1: # Bit 0, V-blank
                print("V-blank")
            if intf & 0x2: # Bit 1, LCDC
                print("LCDC")
            if intf & 0x4: # Bit 2, Timer
                print("Timer")
            if intf & 0x8: # Bit 3, Serial I/O
                print("Serial transfer complete")
            if intf & 0x10: # Bit 4, Pin flip
                print("Bit flip")