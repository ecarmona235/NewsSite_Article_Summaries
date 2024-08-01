# Last edited: 08/01/2024
import unittest
from controller import *
# import pytest



class TestControlller(unittest.TestCase):
    """ Test class for controller file. 
    """
    

    
    def test_UserClass(Self):
        test_user = User(['nbc', 'https://www.nbcnews.com/', 'div', 'related-content-tease__headline', 0], 5)
        
        Self.assertEqual(test_user.site, 'nbc')
        Self.assertEqual(test_user.address, 'https://www.nbcnews.com/')
        Self.assertEqual(test_user.tag, 'div')
        Self.assertEqual(test_user.html_class, 'related-content-tease__headline')
        Self.assertEqual(test_user.skips, 0)
        Self.assertEqual(test_user.numb_requested, 5)
        
        
    # TODO: Figure out how to test the user api calls. 
        
    
    
    
    
if __name__ == '__main__':
    unittest.main()