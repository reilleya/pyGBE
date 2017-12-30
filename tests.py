import gblib, time

def testPushPop():
    testCore = gblib.core()
    testCore.reg.setReg('af', 0x01B0)
    testCore.reg.setReg('bc', 0x0013)
    testCore.reg.setReg('de', 0x00D8)
    testCore.reg.setReg('hl', 0x014D)
    testCore.reg.setReg('sp', 0x0009)
    testCore.reg.setReg('pc', 0x0000)
    
    testCore.rom = [0xf3, 0xf5, 0x97, 0x47, 0x48, 0xc1, 0x0, 0x0, 0x0]
    
    for i in range(0, 7):
        testCore.reg.dumpState('x')
        print(testCore.rom)
        testCore.loop()

def testReset():
    testCore = gblib.core()
    testCore.reg.setReg('af', 0x01B0)
    testCore.reg.setReg('bc', 0x0013)
    testCore.reg.setReg('de', 0x00D8)
    testCore.reg.setReg('hl', 0x014D)
    testCore.reg.setReg('sp', 0x0014)
    testCore.reg.setReg('pc', 0x0000)
    
    testCore.rom = [0xf3, 0xd7, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,
                    0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xd7, 0x0, 0x0]
    
    for i in range(0, 20):
        testCore.loop()
        testCore.reg.dumpState('x')
        print(testCore.rom)

if __name__ == '__main__':
    testReset()