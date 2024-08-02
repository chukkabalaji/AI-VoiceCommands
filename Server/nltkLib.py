from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from fuzzywuzzy import fuzz

if __name__== "__main__":    
    query = word_tokenize("I am feeling bad")
    stop_words = set(stopwords.words("english"))

    ratio = fuzz.ratio('Could you please submit a trade', 'book a trade')
    print(ratio)
    ratio = fuzz.token_set_ratio('Could you submit a trade', 'book a trade')
    print(ratio)
    # for lemma in wn.synset('book the trade').lemmas():
    #     print(lemma.name())
    
    # for q in query:
    #     if q.casefold() not in stop_words:
    #         print(q)

    # print(query)