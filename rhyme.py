from score import prepare_model,predict

def rhyme(wordToRhyme, d, dict, model, tokenizer, treshold, amount):
    # Define the word for which you want to generate rhymes
    word = wordToRhyme
    if dict.check(wordToRhyme) == False:
        return []

    # Get the phoneme representation of the word
    phones = d[word][0]

    # Create a set to store the rhymes
    rhymes = set()

    # Iterate through the words in the dictionary
    for word, pron in d.items():
        # Check if the word is not the original word
        if word != wordToRhyme:
            # Get the phoneme representation of the word
            phones2 = pron[0]
            # Check if the word rhymes with the original word
            if phones[-2:] == phones2[-2:]:
                if dict.check(word):
                    rhymes.add(word)

    list = []
    for rhyme in rhymes:
        list.append([rhyme, wordToRhyme])

    final = predict(list, model, tokenizer, treshold, amount)
    for item in final:
        item['score'] = str(item['score'])
    return final


