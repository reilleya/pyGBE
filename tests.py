import gblib, time

def makeTestRom(prog, rtype):
    rom = [0] * 32768
    rom[0x0134:0x0141] = [ord('T'), ord('E'), ord('S'), ord('T'), ord(' '), ord('R'), ord('O'), ord('M')]
    rom[0x0147] = rtype
    rom[0x0100] = 0
    rom[0x0101:0x0103] = [0xC3, 0x50, 0x01]

    for i in range(0, len(prog)):
        rom[0x0150 + i] = prog[i]

    return rom

def testPushPop():
    prog = [0xC5, 0xF1]
    rom = makeTestRom(prog, 0)
    testCore = gblib.core(romdata = rom)
    testCore.reg.setReg('af', 0x01B0)
    testCore.reg.setReg('bc', 0x0013)
    testCore.reg.setReg('de', 0x00D8)
    testCore.reg.setReg('hl', 0x014D)
    testCore.reg.setReg('sp', 0xFFFE)
    testCore.reg.setReg('pc', 0x0100)
    
    print("Start: ")
    testCore.reg.dumpState('x')
    print()

    print("Run: ")
    for i in range(0, len(prog) + 2):
        testCore.loop()
        testCore.reg.dumpState('x')

if __name__ == '__main__':
    testPushPop()