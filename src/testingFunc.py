#Made by Cody
import unittest
import map
import map._map_getters_setters
import numpy
import map.cell as cell

mapTesting = map.Map(8,7)
posGrid = numpy.zeros((8,7), dtype = (int,2))
mapTesting.setCell((0,0),color=cell.RED, type=cell.UNIT, strength=1, resources=20, isdisabled=True)

class TestingCases(unittest.TestCase):

 
    def testCellDiemnsion(self):
                self.assertEqual(mapTesting.getDimensions(), (8,7))
    def testGetColor(self):
                self.assertEqual(mapTesting.getColor((0,0)), cell.RED)
    def testGetType(self):
                self.assertEqual(mapTesting.getType((0,0)), cell.UNIT)
    def testGetStrength(self):
                self.assertEqual(mapTesting.getStrength((0,0)), 1)
    def testGetAdjacent(self):
                self.assertEqual(mapTesting.getAdjacent((0,0)), [(1,0),(0,1)])
                self.assertEqual(mapTesting.getAdjacent((1,2)), [(0,2),(2,2),(1,3),(1,1),(0,1),(0,3)])
                self.assertEqual(mapTesting.getAdjacent((7,2)), [(6,2),(7,3), (7,1),(6,1),(6,3)])
    def testGetResources(self):
                self.assertEqual(mapTesting.getResources((0,0)), 20)
    def testGetDisabled(self):
                self.assertEqual(mapTesting.getDisabled((0,0)), True)
    def testGetRGB(self):
                self.assertEqual(mapTesting.getRGB((0,0)), (0,0,0)) 

		
		
if __name__ == '__main__':
    unittest.main()		
