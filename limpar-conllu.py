# -*- coding: utf-8 -*-

import sys

def limpar(texto):
	novotexto = list()
	for linha in texto.splitlines():
		if "# text" in linha:
			novotexto.append(linha.split('# text = ')[1])

	return "\n".join(novotexto)

def main(antes, depois, codificação = "utf8", codificação2 = "utf-8"):
	antes = open(antes, 'r', encoding=codificação).read()
	open(depois, 'w', encoding=codificação2).write(limpar(antes))

if __name__ == "__main__":
	if len(sys.argv) == 2 and sys.argv[1] == '--atualizar':
		import atualizar_repo
		atualizar.atualizar()
		print('Atualizado com sucesso!')
		exit()
	if len(sys.argv) < 3:
		print("uso: limpar-conllu.py --atualizar UD.conllu texto.txt codificação-original* codificação-nova*\n* A codificação é opcional")
	elif len(sys.argv) == 3: 
		main(sys.argv[1], sys.argv[2])
		print('OK!')
	elif len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
		print('OK!')
	elif len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
		print('OK!')
	else:
		print("Argumentos excessivos")
