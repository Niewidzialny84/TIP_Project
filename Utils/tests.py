import unittest

from packerTests import PackerTests
from serverTests import ServerTests
from udpTests import udpTests

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PackerTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ServerTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(udpTests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())