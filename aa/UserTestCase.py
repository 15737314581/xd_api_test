import unittest


class UserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUp.....")
    @classmethod
    def tearDownClass(cls):
        print("tearDown...")

    def testCase1(self):
        print("testCase1....")

    # @unittest.skip("跳过")
    def testCase2(self):
        print("testCase2....")
        self.assertEqual(1,1)

    def testCase3(self):
        print("testCase3....")
        self.assertEqual(2,2)

if __name__ == '__main__':
    # unittest.main(verbosity=1)
    suite = unittest.TestSuite()
    # suite.addTests([UserTestCase("testCase2"),UserTestCase("testCase1"),UserTestCase("testCase3")])
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(UserTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
