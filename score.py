import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer

import pandas as pd

MAX_LEN = 64
def tokenize_inputs(phrase_a, phrase_b, tokenizer):

    tokenized_phrases = tokenizer.texts_to_sequences([phrase_a, phrase_b])

    # now loop through inputs and pad or reduce size if required
    tokenized_phrases_for_output = []
    for phrase in tokenized_phrases:
        if len(phrase) < MAX_LEN:
            length_to_pad = MAX_LEN - len(phrase)
            phrase_for_output = ([0] * length_to_pad) + phrase
        elif len(phrase) > MAX_LEN:
            phrase_for_output = phrase[-MAX_LEN:]
        else:
            phrase_for_output = phrase
        tokenized_phrases_for_output.append(phrase_for_output)

    return tf.constant(tokenized_phrases_for_output, dtype=tf.float64)
def prepare_model():
    rhyme_df = pd.read_csv('data/rhymes/rhyme_df.csv')
    rhyme_df = rhyme_df.dropna(subset=['word_a', 'word_b', 'rhyme'])
    non_rhyme_df = pd.read_csv('data/rhymes/non_rhyme_df.csv')
    non_rhyme_df = non_rhyme_df.dropna(subset=['word_a', 'word_b', 'rhyme'])
    df = pd.concat([
            rhyme_df.sample(400_000, random_state=123), 
            non_rhyme_df.sample(400_000, random_state=123)
        ])
    del rhyme_df, non_rhyme_df
    df.head()
    # load the model
    model = load_model("rhyme_model.hdf5")
    tokenizer = Tokenizer(char_level=True, lower=True)
    tokenizer.fit_on_texts(df['word_a'] + df['word_b'])
    return model,tokenizer 

def predict(samples, model , tokenizer, treshold, amount):
    sample_tokens = [tokenize_inputs(lyrics[0], lyrics[1], tokenizer) for lyrics in samples]
    sample_tokens = tf.convert_to_tensor(sample_tokens)
    sample_pred = model.predict([sample_tokens[:, 0], sample_tokens[:, 1]])
    predictions = [round(pred[0], 4) for pred in sample_pred]
    list = []
    for i in range(len(samples)):
        if(predictions[i] > float(treshold)):
            list.append({'word' : samples[i][0], 'score' : predictions[i]})
    list_sorted = sorted(list, key=lambda p: p['score'])
    return list_sorted[-int(amount):] 

