from web_package.tests.post_test import PostTestCase

import unittest


if __name__ == '__main__':

    # Prepare all Unit Testing Suites
    post_test_suite = PostTestCase.get_suite()

    # Collect all tests into one testing suite.
    allTests = unittest.TestSuite([post_test_suite])

    # Create a test suite runner
    runner = unittest.TextTestRunner(verbosity=2)
    # Run the test suite and output human readable results
    runner.run(allTests)


    

    # dumb =  PostTestCase('test_dumb')
    # other = PostTestCase('test_other')

    # post_test_suite.addTest(dumb)
    # post_test_suite.addTest(other)

    # suite = unittest.TestLoader().loadTestsFromTestCase(PostTestCase)
    # #print suite
    # result = unittest.TestResult()

    # runner = unittest.TextTestRunner(erbosity=2)
    # result = runner.run(suite)

    # Alternative method here will be useful for automated test pass checkers. Above method shows printout to humans.
    #suite.run(result)
    #print "\n"
    #print result
    

    
    