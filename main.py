import gblib

testCore = gblib.core()

testCore.execute([0x81])

testCore.parseROM("../roms/bios.gb")