# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, abort, Response
import json
from flask_cors import CORS

import enchant
from nltk.corpus import cmudict

from rhyme import rhyme

# creating a Flask app
app = Flask(__name__)
CORS(app)
dict = enchant.Dict("en_US")

# Create an instance of the CMU pronunciation dictionary
d = cmudict.dict()

@app.route('/', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):

        data = "hello world"
        return jsonify({'data': data})


@app.route('/rhymes/<word>', methods=['GET'])
def disp(word):
    rhymes = rhyme(word, d, dict)
    json_rhymes = jsonify(rhymes)
    return json_rhymes


if __name__ == '__main__':

    app.run(debug=True)
