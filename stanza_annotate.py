import stanza
import os
import sys
from stanza.utils.conll import CoNLL
sys.path.append("/home/elvis/ACDC-UD")
import estrutura_ud

#!pip3 install stanza
#stanza.download('pt')

nlp = stanza.Pipeline('pt')
arquivos = {}
arquivos_cru = {}
diretorio = sys.argv[1]
if os.path.isdir(diretorio):
    for arquivo in os.listdir(diretorio):
        with open(diretorio + "/" + arquivo, encoding="utf-8") as f:
            text = f.read()
            arquivos[arquivo.rsplit(".txt")[0]] = CoNLL.convert_dict(nlp(text).to_dict())
elif os.path.isfile(diretorio):
    arquivo = diretorio
    with open(arquivo, encoding="utf-8") as f:
        text = f.read()
        arquivos[arquivo.rsplit(".txt")[0]] = CoNLL.convert_dict(nlp(text).to_dict())

sentences = []
conllus = {}
for arquivo in sorted(arquivos):
    conllus[arquivo] = []
    for s, sentence in enumerate(arquivos[arquivo]):
        text = " ".join([token[1] for token in sentence if not '-' in token[0]])
        sent_id = arquivo + "-" + str(s+1)
        sentences.append("# sent_id = " + sent_id + "\n# text = " + text + "\n" + "\n".join(["\t".join(token) for token in sentence]))
        conllus[arquivo].append("# sent_id = " + sent_id + "\n# text = " + text + "\n" + "\n".join(["\t".join(token) for token in sentence]))

print("\n\n".join(sentences))