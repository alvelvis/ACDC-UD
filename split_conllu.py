import os

pasta_conllu = input('Pasta onde estão os arquivos .conllu:\n').replace('"','').replace("'","").replace('\\','/').strip()

conllus = list()
for arquivo in os.listdir(pasta_conllu):
	if '.conllu' in arquivo:
		conllus.append(arquivo)

print(conllus)

if os.path.isdir(pasta_conllu + '/documents'):
	print('Pasta "documents" já existe em "' + pasta_conllu + '"')
	exit()
else:
	os.mkdir(pasta_conllu + '/documents')

documents = dict()
for conllu in conllus:
	texto = open(pasta_conllu + '/' + conllu, 'r').read().split('\n\n')
	for sentence in texto:
		if '# sent_id = ' in sentence:
			identificador = sentence.split('# sent_id = ')[1].split('-')[0]
			if not identificador in documents.keys():
				documents[identificador] = list()
			documents[identificador].append(sentence)

documentos_organizados = dict()
for documento in documents.keys():
	if not documento in documentos_organizados.keys():
		documentos_organizados[documento] = list()
	for i in range(len(documents[documento])):
		for sentence in documents[documento]:
			if sentence.split('# sent_id = ')[1].split('-')[1].split()[0] == str(i+1):
				documentos_organizados[documento].append(sentence)

	print(documento)
	open(pasta_conllu + '/documents/' + documento + '.conllu', 'w').write('\n\n'.join(documentos_organizados[documento]) + '\n\n')
