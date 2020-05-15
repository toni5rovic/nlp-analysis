import nltk
import configparser
from nltk.tag import StanfordNERTagger
from functools import reduce

class NerAnalysis:
	def __init__(self):
		self.dict_of_dicts = {}
		self.tokenizer = nltk.tokenize.TweetTokenizer()

		config = configparser.ConfigParser()
		config.read("./config.ini")
		folder = config['NER']['stanford_ner_folder']
		self.stanford_tagger = StanfordNERTagger(folder + '\classifiers\english.muc.7class.distsim.crf.ser.gz',
												 folder + '\stanford-ner.jar',
												 encoding='utf-8')
												 	
	def tag_text(self, text):
		sentences = nltk.sent_tokenize(text)
		tokenized_sentences = [self.tokenizer.tokenize(sent) for sent in sentences]
		classified_sentences = self.stanford_tagger.tag_sents(tokenized_sentences)
		list_to_return = []
		for i in range(len(classified_sentences)):
			classified_sent = classified_sentences[i]
			sentence = sentences[i]
			result = self.process_sent(classified_sent, sentence)
			list_to_return.append(result)
		return list_to_return

	def tokenize_text(self, text):
		sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
		sentences = sentence_tokenizer.tokenize(text)
		return sentences

	def process_sent(self, classified_sentence, sentence):
		sentence_with_info = []
		sentence_part = sentence
		# tokenization
		tokens = self.tokenizer.tokenize(sentence)
		num_of_tokens = len(classified_sentence)
		for index, token_with_tag in enumerate(classified_sentence):
			word = token_with_tag[0]
			ner_tag = token_with_tag[1]
			
			# if len(word) == 1 and not word.isalpha():
			# 	pos_tag = "SYM"

			if ner_tag == 'O' or (ner_tag!='O' and not word.isalpha()):
				if (index == num_of_tokens - 1):
					tup = sentence_part, None
					sentence_with_info.append(tup)
				continue

			token_position_final = None
			sentence_splitting = sentence_part
			current_len = 0
			while True:
				token_position = sentence_splitting.find(word)
				# checking after found position
				good_after = False
				if (token_position + len(word) < len(sentence_splitting)):
					char_after_token = sentence_splitting[token_position + len(word)]
					if (char_after_token.isalpha() == False):
						good_after = True
				else:
					good_after = True

				# checking before found position
				good_before = False
				if token_position > 0:
					char_before_token = sentence_splitting[token_position - 1]
					if (char_before_token.isalpha() == False):
						good_before = True
				else:
					# nothing before the token, so it is a full word
					good_before = True

				if good_before and good_after:
					token_position_final = token_position + current_len
					break

				current_len = token_position + 1
				sentence_splitting = sentence_splitting[(token_position + 1):]

			# at this point we have the position
			# "token_position_final" where the token was found

			# split_sentence is a list of parts
			# which are split around the found token
			split_sentence = sentence_part.split(word, 1)
			part_before = sentence_part[0:token_position_final]
			part_after = sentence_part[(token_position_final + len(word)):]

			# pre token part
			tup = part_before, None
			sentence_with_info.append(tup)

			# token and its tag
			tup = word, ner_tag
			sentence_with_info.append(tup)
		
			sentence_part = part_after

		return sentence_with_info

