from flask import Flask, request, make_response, jsonify
from model import *


app = Flask(__name__)

newsites = ['cnn', 'nbc', 'ap', 'associated-press', 'times', 'ny-times']

class APIError(Exception):
    status_code = 400
    
    def __init__(self, message, status_code=None, paylod=None) -> None:
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = paylod
        
    def to_dict(self) -> dict:
        rv = dict(self.payload or ())
        rv['Error'] = self.message
        return rv
    
class User:
    def __init__(self, info_list,request_n):
        self.site : str = info_list[0]
        self.address : str = info_list[1]
        self.tag: str = info_list[2]
        self.html_class :str = info_list[3]
        self.numb_requested : str = request_n
        self.skips : int = info_list[4]
        
    

@app.errorhandler(APIError)
def handle_API_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/news/<newssite>/<n_articles>', methods=['GET'])
def user(newssite: str, n_articles: str):
    if request.method == 'GET':
        # jsonify res
        # send response.
        if newssite.lower() not in newsites:
            raise APIError("Site provided either not supported or mispelled.", status_code=400)
        if not n_articles.isnumeric() or int(n_articles) <= 0:
            raise  APIError("Problem with n_articles provided. Either not a number or below 1.", status_code=400)
        else:
            newUser = User(getSiteInfo(newssite), int(n_articles))
            soup = getContent(newUser.address)
            headlines_list= getHeadlines(soup, tag=newUser.tag, class_=newUser.html_class)
            if len(headlines_list) == 0:
                raise(APIError("There has been a server error. No headlines were returned.", status_code=500))
            for index in range(0, newUser.numb_requested):
                # check for skipping here, and skip in the front or back depending on number
                print(getSummary(headlines_list[index], newUser.site))
                # check summary if None internal error, else save the summary
            # jsonify responses
            # send response 
        return "Hello!"



if __name__ == "__main__":
    app.run(port=5007)