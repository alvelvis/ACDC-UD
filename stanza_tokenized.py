import stanza
import os
import sys
from stanza.utils.conll import CoNLL
sys.path.append("/home/elvis/ACDC-UD")
import estrutura_ud

#!pip3 install stanza
#stanza.download('pt')

nlp = stanza.Pipeline('pt', tokenize_pretokenized=True)
arquivo = sys.argv[1]
final = sys.argv[2]
with open(arquivo, encoding="utf-8") as f:
    arquivo = f.read()

tokenized = [[token.split("\t")[0] for token in sentence.splitlines() if len(token.split("\t")) > 7 and not '-=' in token.split("\t")[0]] for sentence in arquivo.split("\n\n")]
tokenized = CoNLL.convert_dict(nlp([x for x in tokenized if x]).to_dict())

sentences = []
for s, sentence in enumerate([x for x in tokenized if x]):
    text = arquivo.split("\n\n")[s].split("# text = ")[1].split("\n")[0]
    sent_id = arquivo.split("\n\n")[s].split("# sent_id = ")[1].split("\n")[0]
    for token in arquivo.split("\n\n")[s].splitlines():
        if '-=' in token:
            for t, _token in enumerate(sentence):
                if _token[0] == token.split("-")[0]:
                    sentence.insert(t, [token.split("-=")[0]] + token.split("-=")[1].split("\t")[:-1])
                    break
            continue
    sentences.append("# sent_id = " + sent_id + "\n# text = " + text + "\n" + "\n".join(["\t".join(token) for token in sentence]))

with open(final, "w") as f:
    f.write("\n\n".join(sentences) + "\n\n")