# -*- coding: utf-8 -*-

def LerUD(ud_file):
	if ':' in ud_file: codificação = ud_file.split(':')[1]
	else: codificação = 'utf8'
	ud_file = ud_file.split(':')[0]
	arquivo = open(ud_file, 'r', encoding=codificação).read().split('\n\n')

	for a, sentença in enumerate(arquivo):
		arquivo[a] = arquivo[a].splitlines()
			for b, linha in arquivo[a]:
				if len(linha.split('\t')) == 10:
					arquivo[a][b] = arquivo[a][b].split('\t')

	return arquivo

def EscreverUD(UD, arquivo):
	if ':' in arquivo: codificação = arquivo.split(':')[1]
	else: codificação = "utf8"
	arquivo = arquivo.split(':')[0]

	for a, sentença in enumerate(arquivo):
		for b, linha in enumerate(arquivo[a]):
			if len(linha) == 10 and not '# ' in linha:
				arquivo[a][b] = "\t".join(arquivo[a][b])
			arquivo[a] = "\n".join(arquivo[a])
	arquivo = "\n\n".join(arquivo)

	open(arquivo, 'w', encoding=codificação).write(arquivo)


