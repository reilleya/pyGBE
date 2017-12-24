import gblib

testCore = gblib.core()

testCore.reg.dumpState()
testCore.reg.setReg('A', 6)
testCore.reg.dumpState()
testCore.reg.setReg('C', 4)
testCore.reg.dumpState()

testCore.decode(0x81, 0x0)

testCore.parseROM("../roms/bios.gb")