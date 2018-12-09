# -*- coding: utf-8 -*-

import os

arquivo_ids = input('Arquivo de IDs (.txt):\n').replace('"','').replace("'","").strip()
while arquivo_ids.strip() == '':
	arquivo_ids = input('Arquivo de IDs (.txt):\n').replace('"','').replace("'","").strip()

diretorio = arquivo_ids.rsplit('/', 1)[0] + '/'
arquivo_conllu = arquivo_ids.split('.txt')[0] + '.conllu'

ids = open(arquivo_ids, 'r').read()

arquivos_conllu = list()
for conllu in os.listdir(diretorio + 'documents'):
	if os.path.isfile(diretorio + 'documents/' + conllu):
		arquivos_conllu.extend(open(diretorio + 'documents/' + conllu, 'r').read().split('\n\n'))

novo_conllu = list()
for i, identificador in enumerate(ids.splitlines()):
	if identificador.strip() != '':
		for sentence in arquivos_conllu:
			if '# sent_id = ' in sentence and sentence.split('# sent_id = ')[1].split('\n')[0] == identificador:
				novo_conllu.append(sentence)
				print(str(i+1) + '/' + str(len(ids.splitlines())) + ': ' + identificador)
				break

open(arquivo_conllu, 'w').write("\n\n".join(novo_conllu) + '\n\n')

