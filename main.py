import requests
from bs4 import BeautifulSoup 


def getContent(url):
    
    request = requests.get(url=url)
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup

def getLinks(soup, tag, class_):
    ret_arr = []
    for links in soup.find_all(tag, class_=class_):
        ret_arr.append(links.get('href'))
    return ret_arr

def getParagraphs(soup, tag, class_):
    ret_arr = []
    paragraphs = soup.find(tag, class_=class_)
    for lines in paragraphs.get_text().splitlines():
        if lines == ' I Made It':
            break
        if lines != ' Dotdash Meredith Food Studios' and lines != 'Jump to Nutrition Facts' and lines != '':
            ret_arr.append(lines)
    return ret_arr    
        

if __name__ == "__main__":
    soup = getContent('https://www.allrecipes.com/classic-appetizers-for-summer-8653298')
    links = getLinks(soup, 'a', "mntl-sc-block-universal-featured-link__link mntl-text-link button--contained-standard type--squirrel")
    for recepies in links:
        sub_soup = getContent(recepies)
        paragraphs = getParagraphs(sub_soup, 'div', 'comp article-content mntl-block')
        print(paragraphs)
        print('\n')
