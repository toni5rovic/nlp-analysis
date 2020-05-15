import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.chunk import tree2conlltags
from functools import reduce

class NerAnalysis:
	def __init__(self):
		self.dict_of_dicts = {}
		self.tokenizer = nltk.tokenize.TweetTokenizer()

		_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
		self.tagger = nltk.data.load(_POS_TAGGER)

		_MULTICLASS_NE_CHUNKER = 'chunkers/maxent_ne_chunker/english_ace_multiclass.pickle'
		self.multiclass_ner = nltk.data.load(_MULTICLASS_NE_CHUNKER)
	
	def process_text(self, text):
		sentences = nltk.sent_tokenize(text)
		for sentence in sentences:
			tokens = self.tokenizer.tokenize(sentence)
			tags = self.tagger.tag(tokens)
			
			ne_tree_multiclass = self.multiclass_ner.parse(tags)
			iob_tagged_multiclass = tree2conlltags(ne_tree_multiclass)
			self.process_iob_tagged(iob_tagged_multiclass)
	
	def tag_text(self, text):
		list_to_return = []

		sentences = nltk.sent_tokenize(text)
		for sentence in sentences:
			tokens = self.tokenizer.tokenize(sentence)
			tags = self.tagger.tag(tokens)
			
			ne_tree_multiclass = self.multiclass_ner.parse(tags)
			iob_tagged_multiclass = tree2conlltags(ne_tree_multiclass)
			result = self.process_sent(iob_tagged_multiclass, sentence)
			print(result)
			result = self.postprocess_tagged_list(result)
			list_to_return.append(result)
		return list_to_return

	def process_sent(self, tagged_sentence, sentence):
		sentence_with_info = []
		sentence_part = sentence
		# tokenization
		tokens = self.tokenizer.tokenize(sentence)
		num_of_tokens = len(tagged_sentence)
		for index, token_with_tags in enumerate(tagged_sentence):
			word = token_with_tags[0]
			ner_tag = token_with_tags[2]

			if len(ner_tag) == 1:
				if (index == num_of_tokens - 1):
					tup = sentence_part, None
					sentence_with_info.append(tup)
				continue
				
			token_position_final = None
			sentence_splitting = sentence_part
			current_len = 0
			while True:
				token_position = sentence_splitting.find(word)
				#print(word, " -> ", token_position, " -> ", ner_tag)
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

	def postprocess_tagged_list(self, list_of_tagged_parts):
		results = []
		for tagged_part in list_of_tagged_parts:
			text = tagged_part[0]
			tag = tagged_part[1]
			if tag is None:
				results.append(tagged_part)
				continue
			
			ind = tag.find("-")
			tag = tag[ind+1:]
			tup = text, tag
			results.append(tup)
		
		return results

	def process_iob_tagged(self, iob_tagged_multiclass):
		for ind in range(len(iob_tagged_multiclass)):
			iob_entity = iob_tagged_multiclass[ind]
			full_word = iob_entity[0]
			iob = iob_entity[2][0]
			
			if len(iob_entity[2]) == 1:
				continue
			if iob == "I":
				continue
			if iob == "B":
				inner_ind = ind + 1
				iob_entity_part = iob_tagged_multiclass[inner_ind]
				while iob_entity_part[2][0] == "I":
					full_word += " " + iob_entity_part[0]
					
					inner_ind += 1
					iob_entity_part = iob_tagged_multiclass[inner_ind]
						
			# get category
			ind = iob_entity[2].find("-")
			category = iob_entity[2][ind+1:]
			
			self.add_to_dict(category, full_word)