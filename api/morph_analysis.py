import spacy
import unicodedata
from collections import Counter

class MorphologicalAnalysisData:
	def __init__(self):
		self.tokens_num = 0
		self.tokens_unique_num = 0
		self.sents_num = 0
		self.stopwords_num = 0
		self.stopwords_unique_num = 0
		self.top_5_words = []
		self.nouns_num = 0
		self.verbs_num = 0
		self.adjectives_num = 0
	
	def serialize(self):
		return {
			"sentsNum" : self.sents_num,
			"tokensNum" : self.tokens_num,
			"tokensUniqueNum" : self.tokens_unique_num,
			"stopwordsNum" : self.stopwords_num,
			"stopwordsUniqueNum" : self.stopwords_unique_num,
			"top5Words" : self.top_5_words,
			"nounsNum" : self.nouns_num,
			"verbsNum" : self.verbs_num,
			"adjsNum" : self.adjectives_num
		}
	
	def print_all(self):
		print("sentsNum: ", self.sents_num)
		print("tokensNum: ", self.tokens_num)
		print("tokensUniqueNum: ", self.tokens_unique_num)
		print("stopwordsNum: ", self.stopwords_num)
		print("stopwordsUniqueNum: ", self.stopwords_unique_num)
		print("top5Words: ")
		for word, freq in self.top_5_words:
			print("\t", word, " : ", freq)
		print("nounsNum: ", self.nouns_num)
		print("verbsNum: ", self.verbs_num)
		print("adjsNum: ", self.adjectives_num)

class MorphologicalAnalysis:
	def __init__(self):
		self.nlp = spacy.load("en_core_web_sm")
	
	def analyze(self, text):
		text = unicodedata.normalize("NFKD", text)
		data = MorphologicalAnalysisData()
		doc = self.nlp(text)

		# sentences 
		data.sents_num = len(list(enumerate(doc.sents)))

		# tokens
		tokens = [tok.text for tok in doc]
		data.tokens_num = len(tokens)
		unique_tokens = list(set(tokens))
		data.tokens_unique_num = len(unique_tokens)

		# stopwords
		stopwords = [tok.text for tok in doc if tok.is_stop == True]
		data.stopwords_num = len(stopwords)
		unique_stopwords = list(set(stopwords))
		data.stopwords_unique_num = len(unique_stopwords)

		# top 5 words (without stopwords)
		words_no_stop = [tok.text for tok in doc if tok.is_stop == False and tok.is_punct == False]
		word_freq = Counter(words_no_stop)
		common_words = word_freq.most_common(5)
		data.top_5_words = common_words

		# nouns, adjectives, verbs
		nouns = [tok.text for tok in doc if tok.pos_ == "NOUN"]
		data.nouns_num = len(nouns)
		adjs = [tok.text for tok in doc if tok.pos_ == "ADJ"]
		data.adjectives_num = len(adjs)
		verbs = [tok.text for tok in doc if tok.pos_ == "VERB"]
		data.verbs_num = len(verbs)

		return data