# Last edited: 08/01/2024
from flask import Flask, request, jsonify
from model import *


app = Flask(__name__)

NEWSSITES = ['cnn', 'nbc', 'ap', 'associated-press', 'times', 'ny-times']

class APIError(Exception):
    """Error handling class for handling API errors."""
    status_code = 400
    
    def __init__(self, message, status_code=None, paylod=None) -> None:
        """Initiates error message.

        Args:
            message (str): Description of error. 
            status_code (str, optional): Status code used for error. Defaults to 400.
            paylod ( optional): Anything that needs to be sent with the error message. Defaults to None.
        """
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = paylod
        
    def to_dict(self) -> dict:
        """Prepares an error dictionary with message and payload,

        Returns:
            dict: Returns a dictionary to be JSONIFY and returned
        """
        rv = dict(self.payload or ())
        rv['Error'] = self.message
        return rv

@app.errorhandler(APIError)
def handle_API_errors(error):
    """API error handler. Will return the JSONIFY response to user. 

    Args:
        error (str): Description of error. 

    Returns:
        JSON : Returns error response with proper status code. 
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

   
class User:
    """User class, saves all properties of user request. 
        Attributes
        ---------
        site : str : name of news site requested
        address : str : formatted address to the site requested
        tag: str : tag of where headlines are found
        html_class :str : class where the headlines are found
        numb_requested : str : number of articles requested by user
        skips : int : conditional number whether parts of the headline 
        response should be skipped. If negative it will skip from the end, 
        else from the beginning. 
        
    """
    def __init__(self, info_list,request_n):
        """

        Parameters:
            info_list (list): A list containing
                 - the site reqested
                 - the address to site requested
                 - the html tag 
                 - the html class 
                 - skips
            request_n (str): number of articles requested. 
        """
        self.site : str = info_list[0]
        self.address : str = info_list[1]
        self.tag: str = info_list[2]
        self.html_class :str = info_list[3]
        self.numb_requested : str = request_n
        self.skips : int = info_list[4]
        
    

@app.route('/news/<newssite>/<n_articles>', methods=['GET'])
def user(newssite: str, n_articles: str):
    """ Main api route. Will handle incoming requested and return the proper response. 

    Args:
        newssite (str): site requested by user.
        n_articles (str): number of articles requested by user.

    Raises:
        APIError: Site provided either not supported or mispelled, status_code=400
        APIError: Problem with n_articles provided. Either not a number or below 1, status_code=400
        APIError: There has been a server error. No headlines were returned, status_code=500
        APUError: There has been a server error. No summaries was returned, status_code=500
    Returns:
        JSON: JSON response containing the summaries of the number of articles requested. 
    """
    if request.method == 'GET':
        # jsonify res
        # send response.
        if newssite.lower() not in NEWSSITES:
            raise APIError("Site provided either not supported or mispelled.", status_code=400)
        if not n_articles.isnumeric() or int(n_articles) <= 0:
            raise  APIError("Problem with n_articles provided. Either not a number or below 1.", status_code=400)
        else:
            newUser = User(getSiteInfo(newssite), int(n_articles))
            soup = getContent(newUser.address)
            headlines_list= getHeadlines(soup, tag=newUser.tag, class_=newUser.html_class)
            stories_dict = {}
            if len(headlines_list) == 0:
                raise(APIError("There has been a server error. No headlines were returned.", status_code=500))
            for index in range(0, newUser.numb_requested):
                if newUser.skips > 0 and index < newUser.skips:
                    # if skips are positive it will skip a number of returned headlines due to scrapping
                    # non-headlines
                    continue
                elif newUser.skips < 0 and index == abs(newUser.skips + len(headlines)):
                    # if skips is negative, it will stop early to skip non headlines.
                    break
                else:
                    stories_dict[headlines_list[index]] = getSummary(headlines_list[index], newUser.site)
                    if stories_dict[headlines_list[index]] is None:
                        raise (APIError("There has been a server error. No summary was returned.", status_code=500))
            return jsonify({f'{newUser.site.upper()} news articles': stories_dict})



if __name__ == "__main__":
    app.run(port=5022)