# -*- coding: utf-8 -*-

import os
import sys
import estrutura_ud

if len(sys.argv) < 2:
	pasta = input("Diretório onde estão os arquivos de id e a pasta documents: ")
else:
	pasta = sys.argv[1]

for arquivo_id in os.listdir(pasta):
	if any(x in arquivo_id for x in ['-test', '-train', '-dev']) and ".txt" in arquivo_id:
		arquivo_ids = pasta + '/' + arquivo_id
		diretorio = arquivo_ids.rsplit('/', 1)[0] + '/'
		arquivo_conllu = arquivo_ids.split('.txt')[0] + '.conllu'

		ids = open(arquivo_ids, 'r').read()

		arquivos_conllu = str()
		for conllu in os.listdir(diretorio + 'documents'):
			if os.path.isfile(diretorio + 'documents/' + conllu):
				arquivos_conllu += open(diretorio + 'documents/' + conllu, 'r').read() + "\n\n"

		corpus = estrutura_ud.Corpus()
		corpus.build(arquivos_conllu)

		novo_conllu = list()
		for i, identificador in enumerate(ids.splitlines()):
			if identificador.strip() != '':
				novo_conllu.append(corpus.sentences[identificador].to_str())
				#print(arquivo_conllu.rsplit('/', 1)[1] + ' - ' + str(i+1) + '/' + str(len(ids.splitlines())) + ': ' + identificador)

		open(arquivo_conllu, 'w').write("\n\n".join(novo_conllu) + '\n\n')
