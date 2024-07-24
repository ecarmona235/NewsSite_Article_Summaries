from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route('/news/<newssite>/<n_articles>', methods=['GET'])
def user(newssite, n_articles):
    if request.method == 'GET':
        # error handling for no newssite, no article number
        # run through model 
        # error handling for proper response from model
        # jsonify response
        # send response.
        return "Hello!"



if __name__ == "__main__":
    app.run(port=5000)