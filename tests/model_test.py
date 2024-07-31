import unittest
from model import *

class TestModel(unittest.TestCase):
    test_soup = getContent('https://www.nbcnews.com/')
    test_headlines = getHeadlines(test_soup, 'div', 'related-content-tease__headline')
    
    def test_getContent(self):
        # bad call
        self.assertEqual(getContent('https://docs.python.org/3/library/unittest.htmlx').title.string, '404 Not Found')
        # good call
        self.assertNotEqual(getContent('https://docs.python.org/3/library/unittest.html').title.string, '404 Not Found')
    
    def test_getHeadlines(self):
        # good call
        self.assertGreater(len(getHeadlines(self.test_soup, 'div', 'related-content-tease__headline')), 0)
        # bad call
        self.assertEqual(len(getHeadlines(self.test_soup, 'span', 'related-content-tease__headline')), 0)
    
    def test_getSiteInfo(self):
        self.assertEqual(getSiteInfo('nbc'), ['nbc', 'https://www.nbcnews.com/', 'div', 'related-content-tease__headline', 0])
        self.assertEqual(getSiteInfo('cnn'), ['cnn', 'https://edition.cnn.com/,', 'span', 'container__headline-text', 0])
        self.assertEqual(getSiteInfo('ap'), ['associated-press', 'https://apnews.com/', 'span', 'PagePromoContentIcons-text', 1])
        self.assertEqual(getSiteInfo('times'), ['ny-times', 'https://www.nytimes.com/#site-content', 'div', 'css-xdandi', -5])
        self.assertEqual(getSiteInfo('badsite'), [])
        
    def test_getSummary(self):
        self.assertGreater(len(getSummary(self.test_headlines[1], 'nbc')), 0)
        
    
if __name__ == '__main__':
    unittest.main()