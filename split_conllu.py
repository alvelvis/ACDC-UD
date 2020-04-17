import os
import re
import sys
import shutil

if len(sys.argv) == 1:
	pasta_conllu = input('Arquivo .conllu:\n').replace('"','').replace("'","").replace('\\','/').strip()
else:
	pasta_conllu = sys.argv[1]

conllus = [pasta_conllu.rsplit('/', 1)[1]] if '/' in pasta_conllu else [pasta_conllu]
#for arquivo in os.listdir(pasta_conllu):
#	if '.conllu' in arquivo:
#		conllus.append(arquivo)
pasta_conllu = pasta_conllu.rsplit('/', 1)[0] if '/' in pasta_conllu else '.'
print(conllus)

if os.path.isdir(pasta_conllu + '/documents/'):
	for item in os.listdir(pasta_conllu + '/documents/'):
		if '.conllu' in item:
			os.remove(pasta_conllu + '/documents/' + item)
else:
	os.mkdir(pasta_conllu + '/documents/')

documents = dict()
for conllu in conllus:
	texto = open(pasta_conllu + '/' + conllu, 'r', encoding="utf8").read().split('\n\n')
	for sentence in texto:
		if '# sent_id = ' in sentence:
			identificador = sentence.split('# sent_id = ')[1].split("\n")[0].rsplit('-', 1)[0]
			if not identificador in documents.keys():
				documents[identificador] = dict()
			documents[identificador][int(sentence.split('# sent_id = ')[1].split("\n")[0].rsplit('-', 1)[1].split()[0])] = sentence

documentos_organizados = dict()
for documento in documents.keys():
	if not documento in documentos_organizados.keys():
		documentos_organizados[documento] = list()
	i = 0
	while documents[documento]:
		i += 1
		if i in documents[documento] and documents[documento][i].split('# sent_id = ')[1].split("\n")[0].rsplit('-', 1)[1].split()[0] == str(i):
			documentos_organizados[documento].append(documents[documento][i])
			del documents[documento][i]
			i = 0

	documento_original = documento
	if len(sys.argv) > 2 and sys.argv[2] == "UD_Portuguese-Bosque":
		nome = re.search(r'\d+', documento)[0]
		for i in range(4 - len(nome)):
			nome = '0' + nome
		documento = re.search(r'\D+', documento)[0] + nome

	print(documento)
	open(pasta_conllu + '/documents/' + documento + '.conllu', 'w', encoding="utf8").write('\n\n'.join(documentos_organizados[documento_original]) + '\n\n')
