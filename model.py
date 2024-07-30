from openai import OpenAI
import requests
from bs4 import BeautifulSoup 
from tokens import YOUR_API_TOKEN, YOUR_ORG_TOKEN


client = OpenAI(
    organization=YOUR_ORG_TOKEN,
    api_key=YOUR_API_TOKEN
    )


def getContent(url):
    request = requests.get(url=url)
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup

def getHeadlines(soup: BeautifulSoup, tag, class_):
    ret_arr = []
    for links in soup.find_all(tag, class_=class_):
        ret_arr.append(links.get_text())
    return ret_arr


def getSummary(headLine: str, site: str):
    content = f"Explain to me the given article from {site.upper()} in a simple way."
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": content
        },
        {
        "role": "user",
        "content": headLine
        }
    ],
    temperature=0.3,
    max_tokens=310,
    top_p=1
    )
    return response.choices[0].message.content

def getSiteInfo(site:str):
    if site.lower() == 'cnn':
        return ['cnn', 'https://edition.cnn.com/,', 'span', 'container__headline-text', 0]
    elif site.lower() == 'nbc':
        return ['nbc', 'https://www.nbcnews.com/', 'div', 'related-content-tease__headline', 0]
    elif site.lower() == 'ap' or site.lower() == 'associated-press':
        return ['associated-press', 'https://apnews.com/', 'span', 'PagePromoContentIcons-text', 1]
    elif site.lower() == 'times' or site.lower() == 'ny-times' :
        return ['ny-times', 'https://www.nytimes.com/#site-content', 'div', 'css-xdandi', -5]
    else:
        return [] # error - unlikely should be caught before this.
    
 

if __name__ == "__main__":
    soup = getContent('https://www.nbcnews.com/')
    headlines = getHeadlines(soup, 'div', "related-content-tease__headline")
    print(getSummary(headlines[1], 'NBC'))
    
   
