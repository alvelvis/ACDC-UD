import stanza
import pickle
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
    if not os.path.isfile(diretorio + "/" + diretorio + ".p"):
        for arquivo in os.listdir(diretorio):
            if arquivo.endswith(".txt"):
                with open(diretorio + "/" + arquivo, encoding="utf-8") as f:
                    text = f.read()
                try:
                    arquivos[arquivo.rsplit(".txt")[0]] = nlp(text)
                except:
                    print('erro: ' + arquivo)
        with open(diretorio + "/" + diretorio + ".p", "wb") as f:
            f.write(pickle.dump(arquivos))
    else:
        with open(diretorio + "/" + diretorio + ".p", "rb") as f:
            arquivos = pickle.load(arquivos)
    for arquivo in arquivos:
        arquivos[arquivo] = CoNLL.convert_dict(arquivos[arquivo].to_dict())
elif os.path.isfile(diretorio):
    arquivo = diretorio
    if not os.path.isfile(diretorio + ".p"):
        with open(arquivo, encoding="utf-8") as f:
            text = f.read()
        arquivos[arquivo.rsplit(".txt")[0]] = nlp(text)
        with open(diretorio + ".p", "wb") as w:
            w.write(pickle.dump(arquivos))
    else:
        with open(diretorio + ".p") as f:
            arquivos = pickle.load(f)
    for arquivo in arquivos:
        arquivos[arquivo] = CoNLL.convert_dict(arquivos[arquivo].to_dict())

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
