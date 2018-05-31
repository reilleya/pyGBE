class MemoryException(Exception):
    """Raise for any error associated with system memory"""

class memory():
    def __init__(self, core):
        self.core = core
        self.ram = [0] * (0x2000 + 0x7F)            # 
        
    def read(self, loc):
        if loc < 0x8000:                            # Cartridge read
            if self.core.rom is not None:
                return self.core.rom.getAt(loc)
            else:
                raise MemoryException("ROM read with no cartridge loaded")
        
        elif loc < 0xA000:                          # VRAM read
            return None                             # NOP
            
        elif loc < 0xC000:                          # Switchable RAM read
            return None
            
        elif loc < 0xE000:                          # RAM read
            return self.ram[loc - 0xC000]
        
        elif loc < 0xFE00:                          # RAM echo
            return self.ram[loc - 0xFE00]
            
        elif loc < 0xFEA0:                          # OAM read
            return None
            
        elif loc < 0xFF00:                          # Empty?
            return None
            
        elif loc < 0xFF4C:                          # IO ports
            return None
        
        elif loc < 0xFF80:                          # Empty
            return None
            
        elif loc < 0xFFFF:                          # RAM write
            return self.ram[0x2000 + loc - 0xFF80]
            
        elif loc == 0xFFFF:                         # Interrupt buffer read
            return self.core.interruptBuff
            
        else:
            raise MemoryException("Read out of range")
            
    def write(self, loc, value):
        if loc < 0x8000:                            # Cartridge write. Error.
            raise MemoryException("Attempted to write to ROM")
        
        elif loc < 0xA000:                          # VRAM write
            pass                                    # NOP
            
        elif loc < 0xC000:                          # Switchable RAM write
            pass
            
        elif loc < 0xE000:                          # RAM write
            self.ram[loc - 0xC000] = value
        
        elif loc < 0xFE00:                          # RAM echo write
            self.ram[loc - 0xFE00] = value
            
        elif loc < 0xFEA0:                          # OAM write
            pass
            
        elif loc < 0xFF00:                          # Empty?
            pass
            
        elif loc < 0xFF4C:                          # IO ports
            pass
        
        elif loc < 0xFF80:                          # Empty
            pass
            
        elif loc < 0xFFFF:                          # Ram write
            self.ram[0x2000 + loc - 0xFF80] = value
            
        elif loc == 0xFFFF:                         # Interrupt buffer write. Is this legal?
            self.core.interruptBuff = value
            
        else:
            raise MemoryException("Write out of range")