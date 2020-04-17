import stanza
import os
import sys
from stanza.utils.conll import CoNLL
sys.path.append("/home/elvis/ACDC-UD")
import estrutura_ud
import json

#!pip3 install stanza
#stanza.download('pt')

arquivo = sys.argv[1]
final = sys.argv[2]
with open(arquivo, encoding="utf-8") as f:
    arquivo = f.read().split("\n\n")

if os.path.isfile(sys.argv[2] + ".json"):
	with open(sys.argv[2] + ".json") as f:
		tokenized_dict = json.load(f)
else:
    tokenized = [[token.split("\t")[0] for token in sentence.splitlines() if len(token.split("\t")) > 7 and not '-=' in token.split("\t")[0]] for sentence in arquivo]
    print("1/4 dicionário tokenizado: ok")
    nlp = stanza.Pipeline('pt', tokenize_pretokenized=True)
    tokenized_nlp = nlp([x for x in tokenized if x])
    print("2/4 anotação: ok")
    tokenized_dict = tokenized_nlp.to_dict()
    with open(sys.argv[2] + ".json", "w") as f:
        json.dump(tokenized_dict, f)
    print(":: checkpoint :: conversão para dict: salva em json")
tokenized = CoNLL.convert_dict(tokenized_dict)
print("3/4 conversão para CoNLL: ok")

sentences = []
for s, sentence in enumerate([x for x in tokenized if x]):
    metadados = {}
    #text = arquivo[s].split("# text = ")[1].split("\n")[0]
    #sent_id = arquivo[s].split("# sent_id = ")[1].split("\n")[0]
    for token in arquivo[s].splitlines():
        #print(token)
        if token.startswith("# "):
            metadados[token.split("# ", 1)[1].split(" ")[0]] = token.split(" = ", 1)[1]
        if '-=' in token:
            for t, _token in enumerate(sentence):
                if _token[0] == token.split("-")[0]:
                    sentence.insert(t, [token.split("-=")[0]] + token.split("-=")[1].split("\t")[:-1])
                    break
            continue
    sentences.append("\n".join(['# ' + x + ' = ' + metadados[x] for x in metadados]) + "\n" + "\n".join(["\t".join(token) for token in sentence]))
print("4/4 metadados: ok")

with open(final, "w") as f:
    f.write("\n\n".join(sentences) + "\n\n")
