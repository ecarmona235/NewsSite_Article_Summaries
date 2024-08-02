# News Site Article Summaries

This project was a learning project. It was built to practice building APIs and learn
about webscrapping and intergration with openAI. The main feature of the program is to 
scrape selected news sites for the headlines fo their top stories then send them to openAI to receive a summary of the article. The summaries are short often no more than 3 sentences. 

## Requirements

Requirements.txt should give you all necessarry requirements. 

`$: pip install -r requirements.txt`

Another requirement is to have an account with openAI and have your tokens given to you
by openAI in a file named tokens.py.

The file should have just two variables.
`YOUR_ORG_TOKEN = str(your org token from openAI)`
`YOUR_API_TOKEN =str(your org token from openAI)`

These will be utilized by the API. 

*Keep tokens hidden at all times and do not upload them anywhere public.*


## Usage

The application supports the following news sites:
    CNN 
    NBC
    Associated-press or ap
    New York Times as times or ny-times

When making API calls it must contain both the site and number of articles requested. 
The number of articles requested must be greater than 0.

Here is a simple example asking for 3 stories from NBC. 

![Image showing an example]( /Python_Web_Scraper/Python_Web_Scaper/example.png ("Example"))
