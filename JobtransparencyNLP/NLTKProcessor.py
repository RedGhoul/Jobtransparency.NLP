from bs4 import BeautifulSoup
from rake_nltk import Rake
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np

def extractKeyPhrasesFromText(TextIn):
    soup = BeautifulSoup(TextIn)
    htmlFreeText = soup.get_text()
    htmlFreeText.replace("-","")
    htmlFreeText = htmlFreeText.strip()
    r = Rake()
    r.extract_keywords_from_text(htmlFreeText)
    final = []
    for pair in r.rank_list:
        newDic = {}
        newDic["Affinty"] = pair[0]
        newDic["Text"] = pair[1]
        final.append(newDic)
    
    return final

def read_article(Text):
    text_in = Text.split('. ')
    sentences = []
    for x in text_in:
        sentences.append(x.replace("[^a-zA-Z]", " ").split(" "))
    return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    
    return similarity_matrix

def _create_frequency_table(text_string) -> dict:

    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable

def _score_sentences(sentences, freqTable) -> dict:
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average

def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary
# https://becominghuman.ai/text-summarization-in-5-steps-using-nltk-65b21e352b65
def generate_summary(textIn, top_n=5):
    soup = BeautifulSoup(textIn)
    textIn = soup.get_text()
    textIn = textIn.replace("-","")
    textIn = textIn.strip()
    empty = []
    listtextIn = sent_tokenize(textIn)
    for x in listtextIn:
        empty.append(x)
    textIn = ". ".join(listtextIn)
    # 1 Create the word frequency table
    freq_table = _create_frequency_table(textIn)
    # 2 Tokenize the sentences
    sentences = sent_tokenize(textIn)
    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)
    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)
    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.5 * threshold)

    return summary

    