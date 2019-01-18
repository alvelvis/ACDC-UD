# -*- coding: utf-8 -*-

import os

pasta = input('Diretório dos arquivos ID.txt:\n').replace('"','').replace("'","").strip()

tudo_junto = str()

for arquivo_id in os.listdir(pasta):
	if 'pt-' in arquivo_id:
		arquivo_ids = pasta + '/' + arquivo_id
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
						print(arquivo_conllu.rsplit('/', 1)[1] + ' - ' + str(i+1) + '/' + str(len(ids.splitlines())) + ': ' + identificador)
						break

		open(arquivo_conllu, 'w').write("\n\n".join(novo_conllu) + '\n\n')
		tudo_junto += "\n\n".join(novo_conllu) + '\n\n'

