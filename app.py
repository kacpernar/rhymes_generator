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

from rhyme import rhyme, polish_rhyme
from rhymes import get_dictionary, rhymes_generator

def f(wordg):
    if(float(wordg["score"]) >= 0):
        wordg["score"] = ""
        return wordg

# creating a Flask app
app = Flask(__name__)
CORS(app)

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

dict = enchant.Dict("en_US")

# Create an instance of the CMU pronunciation dictionary
d = cmudict.dict()
model,tokenizer = prepare_model()
dicts = {}
dicts['pl'] = get_dictionary('pl', False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rhymes/<word>/<treshold>/<amount>', methods=['GET'])
def disp(word,treshold, amount):
    rhymes = rhyme(word, d, dict,model,tokenizer, treshold, amount)
    my_dictionary = list(map(f, rhymes))
    json_rhymes = jsonify(my_dictionary)
    return json_rhymes

@app.route('/pl/<word>/<level>/<amount>', methods=['GET'])
def dispp(word, level, amount):
    rhymes = polish_rhyme(dicts['pl'], word, level, amount)
    my_dictionary = list(map(f, rhymes))
    json_rhymes = jsonify(my_dictionary)
    return json_rhymes


if __name__ == '__main__':
    # app.run(debug=True)
    FlaskUI(app=app, width=1000, height=700, server="flask", port="5000").run() 

