import unittest
import run       as lmpkit

# just some notes on prboom+ compat levels so I can't botch this
# 
# test_01 -  3 - Doom Ultimate  - Doom 1    - E1L1
# test_02 -  3 - Doom Ultimate  - Doom 1    - E1L1
# test_03 -  3 - Doom Ultimate  - Doom 1    - E1L1
# test_04 - 17 - PRBoom 6       - Doom 1    - E1L1
# test_05 - 16 - PRBoom 5       - Doom 1    - E1L1
# 
# probably they hid this somewhere
# needs must locate when I get a chance

class TestLoads(unittest.TestCase):
    '''
    Just tests basic loading for files into framework
    '''
    def test_01(self):
        lmpkit.createDemoLumpFromFile("test_files/test_01.lmp")
        
    def test_02(self):
        lmpkit.createDemoLumpFromFile("test_files/test_02.lmp")
    
    def test_03(self):
        lmpkit.createDemoLumpFromFile("test_files/test_03.lmp")
        
    def test_04(self):
        lmpkit.createDemoLumpFromFile("test_files/test_04.lmp")        

    def test_05(self):
        lmpkit.createDemoLumpFromFile("test_files/test_05.lmp")
        
class TestLoadedLengths(unittest.TestCase):
    '''
    Tests lengths of loaded files
    '''
    def test_01(self):
        # prboom says 1420 tics
        lmpkit.createDemoLumpFromFile("test_files/test_01.lmp")
        
    def test_02(self):
        # prboom says 2204 tics
        lmpkit.createDemoLumpFromFile("test_files/test_02.lmp")
        
    def test_03(self):
        # prboom says 694 tics
        lmpkit.createDemoLumpFromFile("test_files/test_03.lmp")

    def test_04(self):
        # prboom says ??? tics
        lmpkit.createDemoLumpFromFile("test_files/test_04.lmp")
        
    def test_05(self):
        # prboom says ??? tics
        lmpkit.createDemoLumpFromFile("test_files/test_05.lmp")
        
if __name__ == '__main__':
    unittest.main()