from . import registers
from . import functable as f
from . import cbtable as c
from . import clock
from . import rom
from . import memory
from . import display
from . import interrupts

def tc(num):
    return num - (256 * bool(num & 0x80))

class core():
    def __init__(self, romfile = None, romdata = None):
        self.reg = registers.registers()
        
        self.rom = None
        if romfile is not None:
            with open(romfile, "rb") as rfile:
                self.rom = rom.rom(rfile.read())
        elif romdata is not None:
                self.rom = rom.rom(romdata)
                
        self.mem = memory.memory(self)
        self.int = interrupts.interrupts(self)
        self.clock = clock(self)
        self.disp = display.display(self)
        
        self.cbmode = False
        self.totalCycles = 0
        self.interruptsEnabled = True
        self.interruptBuff = 0x0
    
    def loop(self):
        self.disp.update()
        self.int.update()
        ind = self.reg.getReg('pc')
        if self.cbmode:
            ind -= 1
            print(hex(self.getMem(ind)))
        op = self.getMem(ind)
        #print('Running ' + str(hex(op)) + ' at ' + hex(ind))
        self.decodeAndExec(op, ind)
        #self.checkInterrupts() Disabled for now
    
    def decodeAndExec(self, opc, index):
        step = True
        if self.cbmode:
            ins = c[opc]
            self.cbmode = False
        else:
            ins = f[opc]
        if ins[0] == "add":
            res = self.reg.getReg(ins[1][0]) + self.reg.getReg(ins[1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            if len(ins[2]) == 2:
                h1 = self.reg.getReg(ins[1][0]) >> 8
                h2 = self.reg.getReg(ins[1][1]) >> 8
                self.reg.setBit('f', 'h', (h1 & 0xF) + (h2 & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(ins[1][0]) + self.reg.getReg(ins[1][1]) & 0x10000)
            else:
                self.reg.setBit('f', 'h', (self.reg.getReg(ins[1][0]) & 0xF) + (self.reg.getReg(ins[1][1]) & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(ins[1][0]) + self.reg.getReg(ins[1][1]) & 0x100)
            
        elif ins[0] == "addcn": #Add a constant, for E8
            add = self.getMem(index + ins[1][1])
            res = self.reg.getReg(ins[1][0]) + add
            self.reg.setBit('f', 'z', False)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', (self.reg.getReg(ins[1][0]) & 0xF) + add > 0xF)
            self.reg.setBit('f', 'c', (self.reg.getReg(ins[1][0]) + add) & 0x10000)
            
        elif ins[0] == "addcr": #Addition with carry
            res = self.reg.getReg(ins[1][0]) + self.reg.getReg(ins[1][1]) + self.reg.getBit('f', 'c')
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            if len(ins[2]) == 2:
                h1 = self.reg.getReg(ins[1][0]) >> 8
                h2 = self.reg.getReg(ins[1][1]) + self.reg.getBit('f', 'c') >> 8
                self.reg.setBit('f', 'h', (h1 & 0xF) + (h2 & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(ins[1][0]) + self.reg.getReg(ins[1][1])  + self.reg.getBit('f', 'c') & 0x10000)
            else:
                self.reg.setBit('f', 'h', (self.reg.getReg(ins[1][0]) & 0xF) + (self.reg.getReg(ins[1][1]) & 0xF) > 0xF)
                self.reg.setBit('f', 'c', self.reg.getReg(ins[1][0]) + self.reg.getReg(ins[1][1])  + self.reg.getBit('f', 'c') & 0x100)
            
        elif ins[0] == "sub":
            if type(ins[1][1]) is int:
                sv = self.getMem(index + ins[1][1])
            else:
                sv = self.reg.getReg(ins[1][1])
            res = self.reg.getReg(ins[1][0]) - sv
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', (self.reg.getReg(ins[1][0]) & 0x0F) < sv & 0x0F)
            self.reg.setBit('f', 'c', self.reg.getReg(ins[1][0]) < sv)
            
        elif ins[0] == "sbc":
            res = self.reg.getReg(ins[1][0]) - (self.reg.getReg(ins[1][1]) - self.reg.getBit('f', 'c'))
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', (self.reg.getReg(ins[1][0]) & 0x0F) < (self.reg.getReg(ins[1][1]) - self.reg.getBit('f', 'c') & 0x0F))
            self.reg.setBit('f', 'c', self.reg.getReg(ins[1][0]) < self.reg.getReg(ins[1][1]) - self.reg.getBit('f', 'c'))
        
        elif ins[0] == "and":
            if type(ins[1][1]) is str:
                res = self.reg.getReg(ins[1][0]) & self.reg.getReg(ins[1][1])
            elif type(ins[1][1]) is int:
                res = self.reg.getReg(ins[1][0]) & self.getMem(index + ins[1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', True)
            self.reg.setBit('f', 'c', False)
            
        elif ins[0] == "or":
            res = self.reg.getReg(ins[1][0]) | self.reg.getReg(ins[1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', False)
            self.reg.setBit('f', 'c', False)
            
        elif ins[0] == "xor":
            res = self.reg.getReg(ins[1][0]) ^ self.reg.getReg(ins[1][1])
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', False)
            self.reg.setBit('f', 'c', False)
            
        elif ins[0] == "inc":
            res = self.reg.getReg(ins[1][0]) + 1
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', False)
            self.reg.setBit('f', 'h', self.reg.getReg(ins[1][0]) & 0x0F == 0x00)
        
        elif ins[0] == "inc16": #Needed for 16 bit incs because flags aren't updated?
            res = self.reg.getReg(ins[1][0]) + 1
            
        elif ins[0] == "dec16": #Same as inc16
            res = self.reg.getReg(ins[1][0]) - 1
        
        elif ins[0] == "dec":
            res = self.reg.getReg(ins[1][0]) - 1
            self.reg.setBit('f', 'z', res == 0)
            self.reg.setBit('f', 'n', True)
            self.reg.setBit('f', 'h', self.reg.getReg(ins[1][0]) & 0x0F == 0x0F)
        
        elif ins[0] == "cbmode":
            self.cbmode = True
        
        elif ins[0] == "loadcn":
            res = self.getMem(index + ins[1][0])
        
        elif ins[0] == "loadcn16":
            res = self.getMem(index + ins[1][0]) + (self.getMem(index + ins[1][1]) << 8)
        
        elif ins[0] == "mov":
            res = self.reg.getReg(ins[1][0])
        
        elif ins[0] == "cpl":
            res = self.reg.getReg(ins[1][0]) ^ 0xFF
        
        elif ins[0] == "swap":
            res = ((self.reg.getReg(ins[1][0]) & 0x0F) << 8) + ((self.reg.getReg(ins[1][0]) & 0xF0) >> 8)
        
        elif ins[0] == "jump":
            self.reg.setReg('pc', (self.getMem(index + ins[1][0]) << 8) + self.getMem(index + ins[1][1]))
            step = False
            
        elif ins[0] == "jumpR":
            if (self.reg.getReg('f') & ins[1][0]) == ins[1][1]:
                #step = False <- maybe not?
                jump = tc(self.getMem(index + ins[1][2]))
                self.reg.setReg('pc', self.reg.getReg('pc') + jump)
        
        elif ins[0] == "disInt":
            self.int.disable()
        
        elif ins[0] == "enInt":
            self.int.enable()
            
        elif ins[0] == "saveMem":
            if type(ins[1][2]) is str:
                offset = self.reg.getReg(ins[1][2])
            else:
                offset = self.getMem(index + ins[1][2])
            self.setMem(ins[1][1] + offset, self.reg.getReg(ins[1][0]))
        
        elif ins[0] == "loadMem":
            offset = self.getMem(index + ins[1][1])
            res = self.getMem(ins[1][0] + offset)
        
        elif ins[0] == "ldd":
            self.setMem(self.reg.getReg(ins[1][1]), self.reg.getReg(ins[1][0]))
            res = self.reg.getReg(ins[1][1]) - 1
        
        elif ins[0] == "loadPointer":
            fromReg = ins[1][0][1:]
            res = self.getMem(self.reg.getReg(fromReg))
            self.reg.setReg(fromReg, self.reg.getReg(fromReg) + ins[1][1])
        
        elif ins[0] == "push16":
            self.push16(self.reg.getReg(ins[1][0]))
        
        elif ins[0] == "pop16":
            res = self.pop16()

        elif ins[0] == "ret":
            step = False
            res = self.reg.getReg("pc")
            if ins[1][0] is None:
                res = self.pop16()
                if ins[1][3]:
                    self.int.enable()
                    
            elif bool((self.reg.getReg(ins[1][0]) & ins[1][1]) & ins[1][2]):
                res = self.pop16()
        
        elif ins[0] == "rst":
            val = self.reg.getReg("pc")
            loc = self.reg.getReg("sp")
            self.setMem(loc - 1, val & 0x00FF)
            self.setMem(loc - 2, (val & 0xFF00) >> 8)
            self.reg.setReg("sp", loc - 2)
            res = ins[1][0]
        
        elif ins[0] == "call": # ["call", [reg, mask, care, 1, 2], "pc", 3, 12]
            step = False
            res = self.reg.getReg("pc")
            newAddr = self.getMem(index + ins[1][3]) + (self.getMem(index + self.getMem(ins[1][4])) << 8)
            shouldCall = False
            if ins[1][0] is None:
                shouldCall = True
            elif bool((self.reg.getReg(ins[1][0]) & ins[1][1]) & ins[1][2]):
                shouldCall = True
            if shouldCall:
                print("Going to " + str(hex(newAddr)))
                self.push16(res + 3)
                res = newAddr
        
        elif ins[0] == "nop":
            pass
        
        elif ins[0] == "nimp":
            raise NameError("OP " + str(hex(opc)) + " not implemented!")
            
        else:
            raise NameError("Opcode not found")
        
        if ins[2] is not None:
            if ins[2][0] == "*":
                self.setMem(self.reg.getReg(ins[2][1:]), res)
            elif ins[2][0] == "+":
                if ins[2][1] == "2":
                    self.setMem(self.getMem(index + 1) + (self.getMem(index + 2) << 8), res)
            else:
                self.reg.setReg(ins[2], res)
                
        if step:
            self.reg.setReg('pc', self.reg.getReg('pc') + ins[3])
            
        self.clock.stepCycles(ins[4])
    
    def toggleInterrupts(self, setting):
        self.interruptsEnabled = setting
    
    def getMem(self, index):    # Refactor this away
        return self.mem.read(index)
        
    def setMem(self, index, value):     # Refactor this away
        #print("Saving " + str(hex(value)) + " to " + str(hex(index)))
        self.mem.write(index, value)

    def push(self, value):
        loc = self.reg.getReg("sp")
        self.setMem(loc, value)
        self.reg.setReg("sp", loc - 1)

    def push16(self, value):
        self.push(value & 0x00FF)
        self.push((value & 0xFF00) >> 8)
    
    def pop(self):
        loc = self.reg.getReg("sp") + 1
        self.reg.setReg("sp", loc)
        return self.getMem(loc)

    def pop16(self):
        b1 = self.pop()
        b2 = self.pop()
        return b2 + (b1 << 8)
    
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
