import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest
from logger import get_logger

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

logger = get_logger(__name__)

class TextModel:
    def __init__(self, text):
        if not text:
            raise ValueError("Text must be provided.")
        self.text = text
        self.num_sentences = 6

    def summarize_text(self):
        # Tokenização do texto em frases
        sentences = sent_tokenize(self.text)
        
        # Tokenização das palavras e remoção de stopwords
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(self.text.lower())
        words = [word for word in words if word.isalnum() and word not in stop_words]
        
        # Cálculo da frequência das palavras
        word_frequency = nltk.FreqDist(words)
        
        # Normalização da frequência das palavras
        maximum_frequency = max(word_frequency.values())
        for word in word_frequency.keys():
            word_frequency[word] = (word_frequency[word]/maximum_frequency)
        
        # Cálculo da pontuação das frases
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_frequency.keys():
                    if len(sentence.split(' ')) < 33:  # Limite de palavras na frase
                        if sentence not in sentence_scores.keys():
                            sentence_scores[sentence] = word_frequency[word]
                        else:
                            sentence_scores[sentence] += word_frequency[word]
        
        # Seleção das melhores frases
        summarized_sentences = nlargest(self.num_sentences, sentence_scores, key=sentence_scores.get)
        summarized_text = ' '.join(summarized_sentences)
        
        return summarized_text