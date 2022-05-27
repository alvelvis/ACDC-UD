import sys
sys.path.append("/home/elvis/ACDC-UD")
import estrutura_ud

if len(sys.argv < 3):
    sys.stderr.write("usage: release.conllu workbench_anyversion.conllu")
    exit()

release = estrutura_ud.Corpus(recursivo=True)
release.load(sys.argv[1])
workbench = estrutura_ud.Corpus(recursivo=True)
workbench.load(sys.argv[2])

for sentid, sentence in workbench.sentences.items():
    for t, token in enumerate(sentence.tokens):
        if token.deprel == "appos:parataxis":
            release.sentences[sentid].tokens[t].deprel = "appos:parataxis"
        if token.deprel == "ccomp:parataxis":
            release.sentences[sentid].tokens[t].deprel = "appos:parataxis"
        if token.deprel == "xcomp" and token.upos == "VERB" and token.head_token.upos == "VERB":
            token.deprel = token.head_token.deprel
            token.dephead = token.head_token.dephead
            token.head_token.upos = "AUX"
            token.head_token.deprel = "aux"
            token.head_token.dephead = token.id
            for _t, _token in enumerate(sentence.tokens):
                if _token.upos == "SCONJ" and _token.deprel == "mark" and _token.dephead == token.id:
                    _token.upos = "ADP"
                    _token.deprel = "compound"
                _token.dephead = token.head_token.id

print(release.to_str())
