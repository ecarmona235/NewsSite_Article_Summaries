# Last edited: 08/01/2024

from openai import OpenAI
import requests
from bs4 import BeautifulSoup 
# tokens only saved locally to protect your tokens. 
from tokens import YOUR_API_TOKEN, YOUR_ORG_TOKEN


client = OpenAI(
    organization=YOUR_ORG_TOKEN,
    api_key=YOUR_API_TOKEN
    )


def getContent(url: str) -> BeautifulSoup:
    """ Function retrieves the html elements to be scrapped. 

    Args:
        url (str): Formatted URL for of site to be retrieved

    Returns:
        BeautifulSoup Object: full html content from site requested. 
    """
    request = requests.get(url=url)
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup

def getHeadlines(soup: BeautifulSoup, tag: str, class_: str) -> list:
    """Retrieves the headlines from the given beautiful soup.

    Args:
        soup (BeautifulSoup): Unformatted Beautiful soup of site requested
        tag (str): tag of where all headlines are held in the overall html soup
        class_ (str): class where all the headlines are held in the overall html soup

    Returns:
        list: Returns a list containing headlines. If any errors occur it will just return
        an empty list. 
    """
    ret_arr = []
    for links in soup.find_all(tag, class_=class_):
        ret_arr.append(links.get_text())
    return ret_arr


def getSummary(headLine: str, site: str) -> str:
    """Function takes a headline from a news site and gets a summary of the
    article from OPENAI. 

    Args:
        headLine (str): Headline you want the summary from.
        site (str): The site name the headline originated from. 

    Returns:
        str: Returns a summary of the given headline. Usually about 2-3 sentence paragraph. 
    """
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

def getSiteInfo(site:str) -> list:
    """ Function takes one of the supported site names and returns a list containing
    the neccessary information to retrive the headlines. Will return an empty list
    if site name is not one of the supported sites. 
   

    Args:
        site (str): Name of the news site you which to get article summaries from.

    Returns:
        list:  Contains the original name, site address, html tag, html class, number
    number of skips (in that order). 
    """
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
    
   
