import unittest

from packerTests import PackerTests
from serverTests import ServerTests
from udpTests import udpTests
from encryptionTests import encryptionTests

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PackerTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ServerTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(udpTests))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(encryptionTests))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())