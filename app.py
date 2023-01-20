# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, abort, Response, render_template
import json
from flask_cors import CORS
from score import prepare_model
from flaskwebgui import FlaskUI
import mimetypes

import enchant
from nltk.corpus import cmudict

from rhyme import rhyme


# creating a Flask app
app = Flask(__name__)
CORS(app)

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

dict = enchant.Dict("en_US")

# Create an instance of the CMU pronunciation dictionary
d = cmudict.dict()
model,tokenizer = prepare_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rhymes/<word>/<treshold>/<amount>', methods=['GET'])
def disp(word,treshold, amount):
    rhymes = rhyme(word, d, dict,model,tokenizer, treshold, amount)
    json_rhymes = jsonify(rhymes)
    return json_rhymes


if __name__ == '__main__':
    #app.run(debug=True)
    FlaskUI(app=app, width=1000, height=700, server="flask", port="5000").run() 