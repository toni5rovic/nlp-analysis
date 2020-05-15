from semantic_analysis import SemanticAnalysis
from morph_analysis import MorphologicalAnalysis
from ner_nltk_analysis import NerAnalysis

def check_if_same(text, s):	
	if (text != s):
		print("--------------------------")
		print("Nisu isti!")
		print("--------------------------")
	else:
		print("OK!")

sem = SemanticAnalysis()
with open(r"E:\Jaen\UJAEN\NLP_Final\practica_final\Slaight Music donation doubles performing arts fund during coronavirus outbreak.txt", "r", encoding="utf-8") as file:
	text = file.read()

# result = sem.disambiguation(text)
# for sen in result:
# 	for tok, syns in sen:
# 		print(tok)
# 		if syns is not None:
# 			for syn in syns:
# 				print("\t", syn)
# count = 0
# result = sem.antonyms(text)
# for sen in result:
# 	for token, synonym in sen:
# 		if synonym is not None:
# 			print("{0:10} \t {1}".format(token, synonym))
# 			count+=1
# morp = MorphologicalAnalysis()
# result = morp.analyze(text)
# result.print_all()

ner = NerAnalysis()
res = ner.tag_text(text)

print("FINAL SENTENCE:")
s = ""
for sen in res:
	for tok, syns in sen:
		s += tok
	s += " "
print(s)

s = s[: (len(s) - 1)]
check_if_same(text, s)

# print("COUNT: ", count)