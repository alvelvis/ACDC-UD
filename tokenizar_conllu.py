# -*- coding: utf-8 -*-

import sys
import re

def limpar(texto):
	novotexto = list()
	for a, linha in enumerate(texto.splitlines()):

		if len(linha.split('\t')) == 10 and not '-' in linha.split('\t')[0]:
			novotexto.append(re.sub(r'^(.*?)\t(.*?)\t.*$', r'\2\t_\t_\t_\t_\t_\t_\t_\t_\t_', linha))

		elif '# text ' in linha:
			novotexto.append(linha)

		elif linha.strip() == '': novotexto.append('')

	return "\n".join(novotexto)

def main(antes, depois):
	if ':' in antes:
		codificação = antes.split(':')[1]
		antes = antes.split(':')[0]
	else:
		codificação = 'utf8'

	if ':' in depois:
		codificação2 = depois.split(':')[1]
		depois = depois.split(':')[0]
	else:
		codificação2 = 'utf8'

	antes = open(antes, 'r', encoding=codificação).read()
	open(depois, 'w', encoding=codificação2).write(limpar(antes))

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1] == '--atualizar':
		import atualizar_repo
		atualizar_repo.atualizar()
		print('Atualizado com sucesso!')
		exit()
	if len(sys.argv) < 3:
		print("uso: tokenizar_conllu.py ud.conllu:utf8 tokenizado.conllu:utf8")
	elif len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
		print('OK!')
	else:
		print("Argumentos excessivos")
