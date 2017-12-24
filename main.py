import gblib

testCore = gblib.core()

testCore.reg.dumpState()
testCore.reg.setReg('A', 16)
#testCore.reg.dumpState()
testCore.reg.setReg('C', 8)
testCore.reg.dumpState()

testCore.decodeAndExec(0x91, 0x0)

testCore.reg.dumpState()

#testCore.parseROM("../roms/bios.gb")