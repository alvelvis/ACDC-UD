import sys
sys.path.append("/home/elvis/ACDC-UD")
import estrutura_ud

corpus = estrutura_ud.Corpus(recursivo=True)
corpus.load(sys.argv[1])

changes_to_be_made = []
for sentid, sentence in corpus.sentences.items():
    for t, token in enumerate(sentence.tokens):
        if token.deprel == "appos:parataxis":
            changes_to_be_made.append({'sentid': sentid, 't': t, 'coluna': 'deprel', 'valor': token.deprel})
        if token.deprel == "ccomp:parataxis":
            changes_to_be_made.append({'sentid': sentid, 't': t, 'coluna': 'deprel', 'valor': token.deprel})
        if token.deprel == "aux" and token.lemma not in ["ir", "estar",  "ter", "haver"]:
            print(token.lemma + " " + token.head_token.lemma)
