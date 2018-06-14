import gblib, time

log = gblib.logger(False, None)

testCore = gblib.core(log, "../roms/tetris.gb")

st = time.time()
for i in range(0, 1000000):
    testCore.loop()
print(time.time() -  st)
print(testCore.clock.time)
    
#log.toConsole = True
#testCore.reg.dumpState('x')
    
#st = time.time()
#testCore.loopUntil("pc", 0x24AD)
#t = time.time() -  st
#print("BP hit")
#log.toConsole = True

#print(testCore.clock)
#print("Actual: " + str(t))
#inp = ""
#while inp != "q":
#    if inp == "j":
#        testCore.clock.stepCycles(456)
#    testCore.loop()
#    testCore.reg.dumpState('x')
#    inp = input()


# Benchmark
"""testCore.parseROM("../roms/sml.gb")
nin = 10000
st = time.time()
for i in range(0, nin):
    testCore.loop()
    #testCore.reg.dumpState('x')
testCore.reg.dumpState('x')
print(testCore.totalCycles)
print(time.time() - st)"""

