import gblib

testCore = gblib.core()

testCore.reg.dumpState()
#testCore.reg.setReg('A', 6)
#testCore.reg.dumpState()
#testCore.reg.setReg('C', 4)
#testCore.reg.dumpState()

testCore.decodeAndExec(0x81, 0x0)

print(testCore.reg.getBit('a', 2))
print(testCore.reg.getBit('a', 1))

testCore.reg.dumpState()

#testCore.parseROM("../roms/bios.gb")