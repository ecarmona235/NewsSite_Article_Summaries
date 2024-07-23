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

def getHeadlines(soup, tag, class_):
    ret_arr = []
    for links in soup.find_all(tag, class_=class_):
        ret_arr.append(links.get_text())
    return ret_arr


def getSummary(headLine, site):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "Explain to me the given article from {site} in a simple way."
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
 
        

if __name__ == "__main__":
    soup = getContent('https://edition.cnn.com/')
    headlines = getHeadlines(soup, 'span', "container__headline-text")
    print(headlines)
    # print(getSummary(headlines[1], 'NY Times'))
    
    
    # CNN - https://edition.cnn.com/, tag = 'span' , class = container__headline-text
    # NBC - https://www.nbcnews.com/ tag=div class=related-content-tease__headline
    # Associated Press - https://apnews.com/ tag=span class= PagePromoContentIcons-text, skip index 0-1
    # NY times - https://www.nytimes.com/#site-content, tag=div class= css-xdandi -skip last 5
    
   
