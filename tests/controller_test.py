import unittest
from controller import *
# import pytest



class TestControlller(unittest.TestCase):
    

    
    def test_UserClass(Self):
        test_user = User(['nbc', 'https://www.nbcnews.com/', 'div', 'related-content-tease__headline', 0], 5)
        
        Self.assertEqual(test_user.site, 'nbc')
        Self.assertEqual(test_user.address, 'https://www.nbcnews.com/')
        Self.assertEqual(test_user.tag, 'div')
        Self.assertEqual(test_user.html_class, 'related-content-tease__headline')
        Self.assertEqual(test_user.skips, 0)
        Self.assertEqual(test_user.numb_requested, 5)
        
    
    
    
    
if __name__ == '__main__':
    unittest.main()