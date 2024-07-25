from flask import Flask, request, make_response, jsonify


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

@app.errorhandler(APIError)
def handle_API_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/news/<newssite>/<n_articles>', methods=['GET'])
def user(newssite: str, n_articles: str):
    if request.method == 'GET':
        # run through model 
        # error handling for proper response from model
        # jsonify response
        # send response.
        if newssite.lower() not in newsites:
            raise APIError("Site provided either not supported or mispelled.", status_code=400)
        elif not n_articles.isnumeric() or int(n_articles) <= 0:
            raise  APIError("Problem with n_articles provided. Either not a number or below 1.", status_code=400)
            
        return "Hello!"



if __name__ == "__main__":
    app.run(port=5000)