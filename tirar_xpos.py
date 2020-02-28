import estrutura_ud
import sys
corpus = estrutura_ud.Corpus()
corpus.load(sys.argv[1])

for sentence in corpus.sentences.values():
    for token in sentence.tokens:
        token.xpos = "_"

print(corpus.to_str())