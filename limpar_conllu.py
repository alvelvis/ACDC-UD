# -*- coding: utf-8 -*-

import sys

def limpar(texto):
	novotexto = list()
	for linha in texto.splitlines():
		if "# text" in linha:
			novotexto.append(linha.split('# text = ')[1])

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
		print("uso: limpar_conllu.py ud.conllu:utf8 texto.txt:utf8")
	elif len(sys.argv) == 3: 
		main(sys.argv[1], sys.argv[2])
		print('OK!')
	else:
		print("Argumentos excessivos")
