import gblib, time

testCore = gblib.core()

testCore.reg.setReg('af', 0x01B0)
testCore.reg.setReg('bc', 0x0013)
testCore.reg.setReg('de', 0x00D8)
testCore.reg.setReg('hl', 0x014D)
testCore.reg.setReg('sp', 0xFFFE)
testCore.reg.setReg('pc', 0x0100)

#testCore.decodeAndExec(0x06, 0x1)

testCore.reg.dumpState('x')

testCore.parseROM("../roms/sml.gb")

nin = 1000

st = time.time()

for i in range(0, nin):
    testCore.loop()
    #testCore.reg.dumpState('x')

testCore.reg.dumpState('x')

print(nin/(time.time() - st))