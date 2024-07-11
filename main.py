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
    # return soup.find(tag, class_=class_)
    for links in soup.find_all(tag, class_=class_):
        ret_arr.append(links.get_text())
    return ret_arr


def getSummary(headLine):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": "Summarize content you are provided with."
        },
        {
        "role": "user",
        "content": headLine
        }
    ],
    temperature=0.7,
    max_tokens=110,
    top_p=1
    )
    return response.choices[0].message.content
 
        

if __name__ == "__main__":
    soup = getContent('https://edition.cnn.com/')
    headlines = getHeadlines(soup, 'span', "container__headline-text")
    # print(headlines)
    print(headlines[15])
    print(getSummary("CNN article: " + headlines[15]))
   
