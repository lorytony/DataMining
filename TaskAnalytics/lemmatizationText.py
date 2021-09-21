import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist, classify, NaiveBayesClassifier


#eliminate emoticon
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def elaborateText(tweet_text):
    #removing urls
    text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                      '(?:%[0-9a-fA-F][0-9a-fA-F]))+','',  tweet_text)
    
    
    #removing emoticon
    text = remove_emoji(text)
    
    text = re.sub("(@[A-Za-z0-9_]+)","", text)
    
    text = text.lower()
    
    for punct_sign in string.punctuation:
        text = text.replace(punct_sign," ")
        
    #others puntuations not within the set of string.punctuation->{!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~}
    text = text.replace("’"," ")
    text = text.replace("”"," ")
    text = text.replace("“"," ")
    text = text.replace("\n"," ")
    
    # removing numbers  
    text = re.sub(r'\d+', '', text)
    
    #tokenaziton
    tokens = nltk.word_tokenize(text)
    
    #removing stopwords
    stopWords = stopwords.words('english')
    filteredTokens = []
    filteredTokens = [word for word in tokens if word not in stopWords]
    
    #lemmatization
    wn.ensure_loaded()

    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    lemmatized_sentence_joined = ""
    tokensTagging = pos_tag(tokens)
    
    # pos tagging & lemmatization
    for word, tag in tokensTagging:

        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
        
    lemmatized_sentence_set = ' '.join(lemmatized_sentence)
  
    return lemmatized_sentence_set




def computeLemmatizationText(dataset,column_name):
    '''

    example dataset:
    index,Tweet Data,Tweet Text,tag
    0,23-08-2021,My Apple phone doesn't work well,negative
    1,23-08-2021,My Apple phone works very well,positive

    using column_name = "Tweet Text",result the following list:
    ["phone not work well","phone work well"]
    
    '''
    lemmatized_set = []

    for row_index in dataset.index:
        row_field = dataset.loc[row_index, column_name]

        filtered_tokens = elaborateText(row_field)

        # lemmatization
        lemmatized_set.append(filtered_tokens)
    return lemmatized_set