import struct

def createDemoLumpFromFile(file):
    ret = DemoLump()
    ret.fromFile(file)
    return ret

class Tic(object):
    # this doubles as my first time trying to use property marker
    # as there's a lot of validation that needs to happen here
    # to have a valid tic
    
    # tic documentation used
    # https://doomwiki.org/wiki/Demo#Doom_2
    def __init__(self):
        # the order here matches the document I'm working with
        # it can be reordered after it's implemented
        self.__forwardBackward = 0
        self.__strafe          = 0
        self.__turn            = 0
        self.__specialMode     = 0
        self.__fireWeapon      = 0
        self.__openDoor        = 0
        self.__swapGun         = 0
        self.__pause           = 0
        self.__save            = 0
        self.__slot            = 0
    
    @property
    def forwardBackward(self):
        return self.__forwardBackward
        
    @forwardBackward.setter
    def forwardBackward(self, value):
        if ((value < -50) or (value > 50)):
            raise ValueError("Can't run forward/backward speed > 50!")
        
        # if we get here, you can set it.
        self.__forwardBackward = value
        
    @property
    def strafe(self):
        return self.__strafe
        
    @strafe.setter
    def strafe(self, value):
        if (not (-50 <= value <= 50)):
            raise ValueError("Can't run strafe with speed > 50!")
        
        if (self.turn != 0):
            if (not (-40 <= value <= 40)):
                raise ValueError("Can't strafe > 50 with turn != 0!")
                
        # if you get here, you can set it.
        self.__strafe = value
        
    @property
    def turn(self):
        return self.__turn
        
    @turn.setter
    def turn(self, value):
        if (value != 0):
            if (not (-40 <= self.strafe <= 40)):
                raise ValueError("Can't strafe > 50 with turn != 0!")
                
        self.__turn = value
        
    @property
    def specialMode(self):
        return self.__specialMode
        
    @specialMode.setter
    def specialMode(self, value):
        self.__specialMode = value

    @property
    def fireWeapon(self):
        return self.__fireWeapon
        
    @fireWeapon.setter
    def fireWeapon(self, value):
        self.__fireWeapon = value
        
    @property
    def openDoor(self):
        return self.__openDoor
        
    @openDoor.setter
    def openDoor(self, value):
        self.__openDoor = value

    @property
    def swapGun(self):
        return self.__swapGun
        
    @swapGun.setter
    def swapGun(self, value):
        self.__swapGun = value
    
    @property
    def pause(self):
        return self.__pause
        
    @pause.setter
    def pause(self, value):
        self.__pause = value
        
    @property
    def save(self):
        return self.__save
        
    @save.setter
    def save(self, value):
        self.__save = value
        
    @property
    def slot(self):
        return self.__slot
        
    @slot.setter
    def slot(self, value):
        # validate
        if (1 == self.save):
            if ((value > 7) or (value < 0)):
                raise ValueError("Save slot must be between 0 and 7!")
        elif (1 == self.swapGun):
            print("DEBUG: Dev is looking for legal gun values")
            print("DEBUG: " + str(value))
        else:
            raise ValueError("Can't have slot set without swapping" +
                             " gun or saving! (set one first)")
        # set if we get here
        self.__slot = value
        
    def fromBytes(self, byte1, byte2, byte3, byte4):
        # this isn't fun, just so we're clear.
        
        # byte1 - movement, is signed
        self.forwardBackward = struct.unpack("b", byte1)[0]
        
        # byte2 - strafing, again, signed
        self.strafe          = struct.unpack("b", byte2)[0]
        
        # byte3 - turning, yet again, signed
        self.turn            = struct.unpack("b", byte3)[0]
        
        # byte4 - a PITA full of PITA stuff.
        # I want this in bits, really
        baseValue = struct.unpack("B", byte4)[0]
        bits = []
        
        # normally I'd do this as a loop
        # I feel lazy and I'm inebriated
        # let's do this lazy but accurate
        
        # 1
        if ((baseValue - 128) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
            baseValue = baseValue - 128
        
        # 2
        if ((baseValue - 64) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
            baseValue = baseValue - 64
        
        # 3
        if ((baseValue - 32) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
            baseValue = baseValue - 32
        
        # 4
        if ((baseValue - 16) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
            baseValue = baseValue - 16
        
        # 5
        if ((baseValue - 8) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
            baseValue = baseValue - 8
        
        # 6
        if ((baseValue - 4) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
            baseValue = baseValue - 4
        
        # 7
        if ((baseValue - 2) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
            baseValue = baseValue - 2
        
        # 8
        if ((baseValue - 1) < 0):
            # bit is zero
            bits.append(0)
        else:
            # bit is 1
            bits.append(1)
        
        # reverse it because docs
        bits.reverse()
        
        # okay, now we can process
        # yes, these are right, it's zero indexed in the docs
        # at https://doomwiki.org/wiki/Demo#Doom_2
        
        # special mode set?
        if (bits[7] == 1):
            # set it so tic can validate itself
            # and set bits to zero so we can validate it, too
            # will be doing this through, so just assume
            bits[7] = 0
            self.specialMode = 1
            
            # changes several behaviors, so check them.
            
            # paused?
            if (bits[0] == 1):
                bits[0] = 0
                self.pause = 1
                
            # save?
            if (bits[1] == 1):
                bits[1] = 0
                self.save = 1
                
                # if saved, slot?
                swp = 0
                swp = swp + (1 * bits[2])
                swp = swp + (2 * bits[3])
                swp = swp + (4 * bits[4])
                
                bits[2] = 0
                bits[3] = 0
                bits[4] = 0
                
                self.slot = swp
                
        else:
            # not special mode in case you missed it
            
            # gun fired
            if (bits[0] == 1):
                bits[0] = 0
                self.fireWeapon = 1
            
            # open door            
            if (bits[1] == 1):
                bits[1] = 0
                self.openDoor = 1
                
            # swap to gun
            if (bits[2] == 2):
                bits[2] = 0
                self.swapGun = 1
                
                # if gun swapped, slot?
                swp = 0
                swp = swp + (1 * bits[3])
                swp = swp + (2 * bits[4])
                swp = swp + (4 * bits[5])
                
                bits[3] = 0
                bits[4] = 0
                bits[5] = 0
                
                self.slot = 0
                
        # at this point, if anything is in the byte, I've missed
        # it and need to know
        if (1 in bits):
            print("script has unrecognized entries!")
            print(bits)
        
    def fromByteString(self, bytestring):
        # eventually, break into bytes and put into
        # frombytes as input but for now...
        pass

class DemoLump(object):
    # difficulties, according to doom source
    SK_BABY      = 0 # I'm too young to die.
    SK_EASY      = 1 # Hey, not too rough.
    SK_MEDIUM    = 2 # Hurt me plenty.
    SK_HARD      = 3 # Ultra-Violence.
    SK_NIGHTMARE = 4 # Nightmare!
    
    def __init__(self):
        self.game_version = 0
        self.skill_level  = 0
        self.episode      = 0
        self.map          = 0
        self.mp_mode      = 0
        self.respawn      = 0
        self.fast         = 0
        self.no_monsters  = 0
        self.pov_player   = 0
        self.has_player_1 = 0
        self.has_player_2 = 0
        self.has_player_3 = 0
        self.has_player_4 = 0
        self.tics         = []
        self.footer       = b""
        
    def addTic(self, tic):
        self.tics.append(tic)
        
    def fromSource(self, fstream):
        # we assume fstream is already open
        # also that it's basically a file
        
        # read the first byte for version
        version_byte = struct.unpack("B", fstream.read(1))[0]
        
        # it must be 109 right now. I don't support any other version.
        if (version_byte != 109):
            raise ValueError("Version must be 109! (Saw " +
                    str(version_byte) + ".)")
        
        # set version now
        self.version = version_byte
        
        # skill_level
        self.skill_level = struct.unpack("B", fstream.read(1))[0]
        
        # episode
        self.episode = struct.unpack("B", fstream.read(1))[0]
        
        # map
        self.map     = struct.unpack("B", fstream.read(1))[0]
        
        # multiplayer
        self.mp_mode = struct.unpack("B", fstream.read(1))[0]
        
        # respawn on
        self.respawn = struct.unpack("B", fstream.read(1))[0]
        
        # fast on
        self.fast    = struct.unpack("B", fstream.read(1))[0]
        
        # no monsters on
        self.no_monsters = struct.unpack("B", fstream.read(1))[0]
        
        # player to view as
        self.pov_player  = struct.unpack("B", fstream.read(1))[0]
        
        # player 1 present
        self.has_player_1 = struct.unpack("B", fstream.read(1))[0]
        
        # player 2 present
        self.has_player_2 = struct.unpack("B", fstream.read(1))[0]
        
        # player 3 present
        self.has_player_3 = struct.unpack("B", fstream.read(1))[0]
        
        # player 4 present
        self.has_player_4 = struct.unpack("B", fstream.read(1))[0]
        
        # load tics
        # ending value for run for tics is raw 0x80
        # see also: http://www.gamers.org/docs/FAQ/lmp.faq.html
        # You're welcome
        while (fstream.peek(1)[:1] != b"\x80"):
            # there are more tics
            swp = Tic()
            
            # just read this out yah? Four bytes.
            swp.fromBytes(fstream.read(1),
                          fstream.read(1),
                          fstream.read(1),
                          fstream.read(1))
            
            # and now we add it back
            self.addTic(swp)
        
        # strip out the end mark
        # I have no doubt there's a "better" way to do this
        # I'm not exactly making production code here
        _garbage = fstream.read(1)
        del _garbage
        
        # the rest is mostly about other things, so I don't care.
        # dump it raw into the footer field
        while (fstream.peek(1) != b""):
            self.footer = self.footer + fstream.read(1)
    
    def fromFile(self, path):
        with open(str(path), "rb") as f:
            self.fromSource(f)
    
def main():
    rec = createDemoLumpFromFile("test_files/test1.lmp")
    print("Test 1")
    print("should be 1420 ticks")
    print("real count...")
    print(len(rec.tics))
    
if __name__ == "__main__":
    main()