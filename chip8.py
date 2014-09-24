import pyglet
import random
import sys

LOGGING = True
def log(msg):
  if LOGGING:
    print msg

#class cpu (pyglet.window.Window):
class cpu:
  inputs = [0] * 16
  display = [0] * 32 * 64
  memory = [0] * 4096
  v = [0] * 16 # 16 8-bit general purpose registers, VF used for special flags
  stack = [] # stack of 16 16-bit values (memory locations)
  opcode = 0
  index = 0 # 16-bit register
  pc = 0 # 16-bit program counter

  def _0NNN(self):
    #log("0NNN")
    extracted_op = self.opcode & 0xf0ff
    try:
      self.funcmap[extracted_op]()
    except:
      #print "Unknown instruction %X" % self.opcode
      pass

  def _00E0(self):
    log("00E0 %X - clear screen" % self.opcode)

  def _00EE(self):
    log("00EE %X - Returns from a subroutine." % self.opcode)

  def _1NNN(self):
    log("1NNN %X - Jumps to address NNN" % self.opcode)
    #self.pc = self.opcode & 0x0fff

  def _2NNN(self):
    log("2NNN %X - Calls subroutine at NNN (incomplete)" % self.opcode)

  def _3XNN(self):
    log("3XNN %X" % self.opcode)

  def _4XNN(self):
    log("4XNN %X - Skips the next instruction if VX doesn't equal NN." % self.opcode)
    if self.v[self.vx] != (self.opcode & 0x00ff):
      self.pc += 2

  def _6XNN(self):
    log("6XNN %X - Sets VX to NN." % self.opcode)
    self.v[self.vx] = self.opcode & 0x00ff

  def _7XNN(self):
    log("7XNN %X - Adds NN to VX" % self.opcode)
    self.v[self.vx] += self.opcode & 0x00ff

  def _ANNN(self):
    log("ANNN %X - Sets I to address NNN" % self.opcode)
    self.index = self.opcode & 0x0fff

  def _DXYN(self):
    log("DXYN %X - Does sprite shit (incomplete)" % self.opcode)

  def _F000(self):
    log("F000 %X - some F---" % self.opcode)
    extracted_op = self.opcode & 0xf0ff
    try:
      self.funcmap[extracted_op]()
    except:
      pass

  def _FX1E(self):
    log("FX1E %X - adds VX to I" % self.opcode)
    self.index += self.v[self.vx]

  def _FX55(self):
    log("FX55 %X - Stores V0 to VX in memory starting at address I." % self.opcode)
    for i in range(16):
      self.memory[self.index+i] = self.v[i]

  def _FX65(self):
    log("FX65 %X - Fills V0 to VX with values from memory starting at address I." % self.opcode)
    for i in range(self.vx):
      self.v[i] = self.memory[self.index+i]


  def load_rom(self, rom_path):
    binary = open(rom_path, "rb").read()
    for i in range(len(binary)):
      self.memory[i+0x200] = ord(binary[i])
    #print self.memory

  def __init__(self, *args, **kwargs):
    #super(cpu, self).__init__(*args, **kwargs)
    self.funcmap = {
      0x0000: self._0NNN,
      0x00E0: self._00E0,
      0x1000: self._1NNN,
      0x2000: self._2NNN,
      0x4000: self._4XNN,
      0x6000: self._6XNN,
      0x7000: self._7XNN,
      0xA000: self._ANNN,
      0xD000: self._DXYN,
      0xF000: self._F000,
      0xF01E: self._FX1E,
      0xF055: self._FX55,
      0xF065: self._FX65
    }



  def cycle(self):
    """ Main loop of emulation """
    self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

    self.vx = (self.opcode & 0x0f00) >> 8
    self.vy = (self.opcode & 0x00f0) >> 4

    extracted_op = self.opcode & 0xf000

    self.pc += 2

    try:
      self.funcmap[extracted_op]()
    except:
      if self.opcode > 0:
        print "Unknown instructon: %X - %X" % (self.opcode, extracted_op)



  def clear(self):
    pass

  def initialize(self):
    self.clear()
    self.inputs 

    self.pc = 0x200

  def main(self):
    self.initialize()
    log(self.pc)
    self.load_rom(sys.argv[1])
    #while not self.has_exit:
    while True:
      #self.dispatch_events()
      self.cycle()
      #self.draw()


  def test(self):
    self.opcode = (self.memory[0+0x200] << 8) | self.memory[0x200+1]
    print self.opcode
    print "0x%X" % self.opcode
    #self.opcode = self.opcode & 0xf000
    #print "0x%X".zfill(2) % self.opcode

emu = cpu()
emu.main()
log("main done")
emu.test()
log("test done")