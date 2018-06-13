class MemoryException(Exception):
    """Raise for any error associated with system memory"""

class memory():
    def __init__(self, core):
        self.core = core
        self.ram = [0] * (0x2000 + 0x7F)            # 0x2000 bytes for 0xC000-0xE000, 0x7f for 0xFF80-0xFF
        
    def read(self, loc):
        if loc < 0x8000:                            # Cartridge read
            if self.core.rom is not None:
                return self.core.rom.read(loc)
            else:
                raise MemoryException("ROM read with no cartridge loaded")
        
        elif loc < 0xA000:                          # VRAM read
            raise MemoryException("VRAM reads not supported " + str(hex(loc)))
            
        elif loc < 0xC000:                          # Switchable RAM read
            raise MemoryException("Switchable RAM reads not supported " + str(hex(loc)))
            
        elif loc < 0xE000:                          # RAM read
            return self.ram[loc - 0xC000]
        
        elif loc < 0xFE00:                          # RAM echo
            return self.ram[loc - 0xFE00]
            
        elif loc < 0xFEA0:                          # OAM read
            raise MemoryException("OAM reads not supported " + str(hex(loc)))

        elif loc < 0xFF00:                          # Empty?
            raise MemoryException("Attempted to read from empty " + str(hex(loc)))
            
        elif loc == 0xFF00:
            print("Warning: Gamepad writes not supported " + str(hex(loc)))
            return 0x00
        
        elif loc < 0xFF03:
            raise MemoryException("Serial reads not supported " + str(hex(loc)))
            
        elif loc < 0xFF08:
            return self.core.clock.read(loc)
        
        elif loc == 0xFF0F:
            return self.core.int.read(loc)
            
        elif loc < 0xFF3F:
            raise MemoryException("Sound reads not supported " + str(hex(loc)))
        
        elif loc < 0XFF4C:
            return self.core.disp.read(loc)
        
        elif loc < 0xFF80:                          # Empty
            raise MemoryException("Attempted to read from empty " + str(hex(loc)))
            
        elif loc < 0xFFFF:                          # RAM write
            return self.ram[0x2000 + loc - 0xFF80]
            
        elif loc == 0xFFFF:                         # Interrupt buffer read
            return self.core.int.read(loc)
            
        else:
            raise MemoryException("Read out of range")
            
    def write(self, loc, value):
        if loc < 0x8000:                            # Cartridge write
            self.core.rom.write(loc, value)
        
        elif loc < 0xA000:                          # VRAM write
            self.core.disp.write(loc, value)
            
        elif loc < 0xC000:                          # Switchable RAM write
            pass
            
        elif loc < 0xE000:                          # RAM write
            self.ram[loc - 0xC000] = value
        
        elif loc < 0xFE00:                          # RAM echo write
            self.ram[loc - 0xFE00] = value
            
        elif loc < 0xFEA0:                          # OAM write
            self.core.disp.write(loc, value)
            
        elif loc < 0xFF00:                          # Empty?
            pass
            
        elif loc == 0xFF00:
            print("Warning: Gamepad writes not supported " + str(hex(loc)))
        
        elif loc < 0xFF03:
            print("Warning: Serial writes not supported " + str(hex(loc)))
            
        elif loc < 0xFF08:
            return self.core.clock.write(loc, value)
        
        elif loc == 0xFF0F:
            return self.core.int.write(loc, value)
            
        elif loc < 0xFF3F:
            print("Warning: Sound writes not supported " + str(hex(loc)))
        
        elif loc < 0XFF4C:
            return self.core.disp.write(loc, value)
        
        elif loc < 0xFF80:                          # Empty
            pass
            
        elif loc < 0xFFFF:                          # Ram write
            self.ram[0x2000 + loc - 0xFF80] = value
            
        elif loc == 0xFFFF:                         # Interrupt buffer write
            self.core.int.write(loc, value)
            
        else:
            raise MemoryException("Write out of range")