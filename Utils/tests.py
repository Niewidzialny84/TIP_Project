import unittest

from packerTests import PackerTests
from serverTests import ServerTests

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PackerTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ServerTests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())