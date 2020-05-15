# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 23:35:13 2020

@author: Toni
"""

from threading import Lock
import nltk
import nltk.tokenize
import os
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from timeit import default_timer as timer
import re

def tokenize(text):
    regEx = "[a-zA-Z]+'?[a-zA-Z]*"
    tokenList = re.findall(regEx, text)
    return tokenList

def synsets_to_str_list(synsets):
    list_of_definitions = []
    for syns in synsets:
        list_of_definitions.append(syns.definition())
    return list_of_definitions

class SemanticAnalysis:
    def __init__(self):
        self.tokenizer = nltk.tokenize.TweetTokenizer()
        # file contents
        self.output_file_content = ""
        self.syn_pairs_file_content = ""
    
    def disambiguation(self, text, pos_tags=["NN", "NNP", "NNS"]):
        # list of lists. each list inside represents a sentence
        # diveded into parts with or without disambiguation 
        list_to_return = []
        sentences = self.tokenize_text(text)
        for sentence in sentences:
            sentence_with_info = []
            # current version of the sentence, 
            # it will change while iterating through tokens
            sentence_part = sentence
            # tokenize
            tokens = self.tokenizer.tokenize(sentence_part)
            tokens_with_tags = nltk.pos_tag(tokens) #
            num_of_tokens = len(tokens)
            #for index, token in enumerate(tokens):
            for index, token_with_tag in enumerate(tokens_with_tags): #
                token = token_with_tag[0] #
                pos_tag = token_with_tag[1] #
                
                if pos_tag not in pos_tags:
                    if (index == num_of_tokens - 1):
                        tup = sentence_part, None
                        sentence_with_info.append(tup)
                    continue
                
                synset_lock = Lock() 
                synset_lock.acquire()
                synsets = wn.synsets(token)
                synset_lock.release()
                if len(synsets) == 0:
                    if (index == num_of_tokens - 1):
                        tup = sentence_part, None
                        sentence_with_info.append(tup)
                    continue

                token_position_final = None
                sentence_splitting = sentence_part
                current_len = 0
                while True:
                    token_position = sentence_splitting.find(token)
                    # checking after found position
                    good_after = False
                    if (token_position + len(token) < len(sentence_splitting)):
                        char_after_token = sentence_splitting[token_position + len(token)]
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

                # split_sentence is a list of parts, 
                # which are split by the token
                split_sentence = sentence_part.split(token, 1)
                part_before = sentence_part[0:token_position_final]
                part_after = sentence_part[(token_position_final + len(token)):]
                
                # pre-token part
                tup = part_before, None
                sentence_with_info.append(tup)
                # token and its synsets
                synsets_string_list = synsets_to_str_list(synsets)
                tup = token, synsets_string_list
                sentence_with_info.append(tup)
                # continuing the processing with the part after the token
                sentence_part = part_after

            list_to_return.append(sentence_with_info)

        return list_to_return

    def synonyms(self, text, pos_tags=["NN", "NNP", "NNS"]):
        list_to_return = []
        # dividing the text into sentences
        sentences = self.tokenize_text(text)
        # parsing sentences
        for sentence in sentences:
            sentence_with_info = []
            sentence_part = sentence
            # tokenization
            tokens = self.tokenizer.tokenize(sentence)
            tokens_with_tags = nltk.pos_tag(tokens)
            num_of_tokens = len(tokens)
            for index, token_with_tag in enumerate(tokens_with_tags):
                word = token_with_tag[0]
                pos_tag = token_with_tag[1]

                if len(word) == 1 and not word.isalpha():
                    pos_tag = "SYM"

                if pos_tag not in pos_tags:
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

                # token and its synonym
                replacement = self.get_replacement(token_with_tag, tokens)
                if replacement is not None:
                    #print("Replacement: ", replacement)
                    tup = replacement, word
                    sentence_with_info.append(tup)
                else:
                    tup = word, None
                    sentence_with_info.append(tup)
                
                sentence_part = part_after
            
            list_to_return.append(sentence_with_info)
        
        return list_to_return

    def antonyms(self, text, pos_tags=["NN", "NNP", "NNS"]):
        list_to_return = []
        # dividing the text into sentences
        sentences = self.tokenize_text(text)
        # parsing sentences
        for sentence in sentences:
            sentence_with_info = []
            sentence_part = sentence
            # tokenization
            tokens = self.tokenizer.tokenize(sentence)
            tokens_with_tags = nltk.pos_tag(tokens)
            num_of_tokens = len(tokens)
            for index, token_with_tag in enumerate(tokens_with_tags):
                word = token_with_tag[0]
                pos_tag = token_with_tag[1]

                if len(word) == 1 and not word.isalpha():
                    pos_tag = "SYM"

                if pos_tag not in pos_tags:
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

                # token and its synonym
                replacement = self.get_antonym(token_with_tag, tokens)
                if replacement is not None:
                    #print("Replacement: ", replacement)
                    tup = replacement, word
                    sentence_with_info.append(tup)
                else:
                    tup = word, None
                    sentence_with_info.append(tup)
                
                sentence_part = part_after
            
            list_to_return.append(sentence_with_info)
        
        return list_to_return
        
    def tokenize_text(self, text):
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sentence_tokenizer.tokenize(text)
        return sentences
    
    def get_replacement(self, token_with_tag, tokens):
        word = token_with_tag[0]
        synset_lock = Lock() 
        synset_lock.acquire()
        synset = lesk(tokens, word)
        synset_lock.release()

        if synset is None:
            return None
        
        lemmas = synset.lemmas()
         # find a replacement
        replacement = None
        for lemma in lemmas:
            lemma_name = lemma.name()
            lemma_pos = lemma.synset().pos()
            if (lemma_pos == 'n') and lemma_name != word:
                replacement = lemma_name
                break
        
        if replacement is None:
            #replacement = word
            return None

        return replacement.replace("_", " ")

    def get_antonym(self, token_with_tag, tokens):
        word = token_with_tag[0]
        synset = lesk(tokens, word)

        if synset is None:
            return None
        
        antonym = None
        for lemma in synset.lemmas():
            if lemma.antonyms():
                antonym = lemma.antonyms()[0].name()
                break

        return antonym