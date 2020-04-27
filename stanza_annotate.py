import stanza
import pickle
import os
import sys
from stanza.utils.conll import CoNLL
#sys.path.append("/home/elvis/ACDC-UD")
import estrutura_ud

#!pip3 install stanza
#stanza.download('pt')

nlp = stanza.Pipeline('pt')
arquivos = {}
arquivos_cru = {}
diretorio = sys.argv[1] if sys.argv[1][-1] != "/" else sys.argv[1].rsplit("/", 1)[0]
sys.stderr.write("\n" + diretorio + "/" + f'{diretorio.rsplit("/", 1)[1] if "/" in diretorio else diretorio}' + ".p")
if os.path.isdir(diretorio):
    if not os.path.isfile(diretorio + "/" + f'{diretorio.rsplit("/", 1)[1] if "/" in diretorio else diretorio}' + ".p"):
        for arquivo in os.listdir(diretorio):
            if arquivo.endswith(".txt"):
                with open(diretorio + "/" + arquivo, encoding="utf-8") as f:
                    text = f.read()
                try:
                    arquivos[arquivo.rsplit(".txt")[0]] = nlp(text)
                except:
                    sys.stderr.write('\nerro: ' + arquivo)
        with open(diretorio + "/" + f'{diretorio.rsplit("/", 1)[1] if "/" in diretorio else diretorio}' + ".p", "wb") as f:
            pickle.dump(arquivos, f)
    else:
        with open(diretorio + "/" + f'{diretorio.rsplit("/", 1)[1] if "/" in diretorio else diretorio}' + ".p", "rb") as f:
            arquivos = pickle.load(f)
    for arquivo in arquivos:
        arquivos[arquivo] = CoNLL.convert_dict(arquivos[arquivo].to_dict())
elif os.path.isfile(diretorio):
    arquivo = diretorio
    if not os.path.isfile(diretorio + ".p"):
        with open(arquivo, encoding="utf-8") as f:
            text = f.read()
        arquivos[arquivo.rsplit(".txt")[0]] = nlp(text)
        with open(diretorio + ".p", "wb") as w:
            pickle.dump(arquivos, w)
    else:
        with open(diretorio + ".p", "rb") as f:
            arquivos = pickle.load(f)
    for arquivo in arquivos:
        arquivos[arquivo] = CoNLL.convert_dict(arquivos[arquivo].to_dict())

sentences = []
conllus = {}
for arquivo in sorted(arquivos):
    conllus[arquivo] = []
    for s, sentence in enumerate(arquivos[arquivo]):
        text = " ".join([token[1] for token in sentence if not '-' in token[0]])
        sent_id = (arquivo + "-" + str(s+1)).rsplit("/", 1)[1] if '/' in arquivo else (arquivo + "-" + str(s+1))
        sentences.append("# sent_id = " + sent_id + "\n# text = " + text + "\n" + "\n".join(["\t".join(token) for token in sentence]))
        conllus[arquivo].append("# sent_id = " + sent_id + "\n# text = " + text + "\n" + "\n".join(["\t".join(token) for token in sentence]))

print("\n\n".join(sentences))
