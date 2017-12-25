import gblib

testCore = gblib.core()

testCore.memory = [1, 7, 6, 7, 6]

#testCore.reg.dumpState()
#testCore.reg.setReg('sp', 1+2+4+8)
#testCore.reg.dumpState()
#testCore.reg.setReg('D', 64)
#testCore.reg.dumpState()

testCore.decodeAndExec(0x06, 0x1)

testCore.reg.dumpState()

#testCore.parseROM("../roms/bios.gb")