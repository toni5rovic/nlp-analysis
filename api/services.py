from semantic_analysis import SemanticAnalysis
from morph_analysis import MorphologicalAnalysis
from ner_nltk_analysis import NerAnalysis

def synonyms(text, pos = 'NOUN'):
	semantic_analysis = SemanticAnalysis()
	result = semantic_analysis.synonyms(text)
	return result

def antonyms(text, pos = 'NOUN'):
	semantic_analysis = SemanticAnalysis()
	result = semantic_analysis.antonyms(text)
	return result

def disambiguation(text):
	semantic_analysis = SemanticAnalysis()
	result = semantic_analysis.disambiguation(text)
	return result

def morphological_analysis(text):
	morpho_analysis = MorphologicalAnalysis()
	result = morpho_analysis.analyze(text)
	return result.serialize()

def ner_analysis(text):
	ner_analysis = NerAnalysis()
	result = ner_analysis.tag_text(text)
	return result

def serialize(list_of_sent_tuples):
	obj = { 'sentList': [] }
	for sentIndex, sent in enumerate(list_of_sent_tuples):
		sent_list = []
		for partIndex, tuple_ in enumerate(sent):
			tags = tuple_[1]
			if (isinstance(tuple_[1], str)):
				l = []
				l.append(tuple_[1])
				tags=l
			item = { 'id': partIndex, 'part': str(tuple_[0]), 'tags': tags}
			sent_list.append(item)
		
		sentence = { 'id': sentIndex, 'sentence': [] }
		sentence['sentence'] = sent_list
		obj['sentList'].append(sentence)
	return obj