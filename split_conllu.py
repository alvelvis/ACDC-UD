import os
import re

pasta_conllu = input('Pasta onde estão os arquivos .conllu:\n').replace('"','').replace("'","").replace('\\','/').strip()

conllus = list()
for arquivo in os.listdir(pasta_conllu):
	if '.conllu' in arquivo:
		conllus.append(arquivo)

print(conllus)

documents = dict()
for conllu in conllus:
	texto = open(pasta_conllu + '/' + conllu, 'r').read().split('\n\n')
	for sentence in texto:
		if '# sent_id = ' in sentence:
			identificador = sentence.split('# sent_id = ')[1].split('-')[0]
			if not identificador in documents.keys():
				documents[identificador] = dict()
			documents[identificador][int(sentence.split('# sent_id = ')[1].split('-')[1].split()[0])] = sentence

documentos_organizados = dict()
for documento in documents.keys():
	if not documento in documentos_organizados.keys():
		documentos_organizados[documento] = list()
	i = 0
	while documents[documento]:
		i += 1
		if i in documents[documento] and documents[documento][i].split('# sent_id = ')[1].split('-')[1].split()[0] == str(i):
			documentos_organizados[documento].append(documents[documento][i])
			del documents[documento][i]
			i = 0

	nome = re.search(r'\d+', documento)[0]
	for i in range(4 - len(nome)):
		nome = '0' + nome
	nome = re.search(r'\D+', documento)[0] + nome


	print(nome)
	open(pasta_conllu + '/documents/' + nome + '.conllu', 'w').write('\n\n'.join(documentos_organizados[documento]) + '\n\n')
