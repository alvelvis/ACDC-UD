# -*- coding: utf-8 -*-

import sys

def main(comparação, revisado):
	#codificação
	if ':' in comparação:
		codificação = comparação.split(':')[1]
		comparação = comparação.split(':')[0]
	else: codificação = 'utf8'
	if ':' in revisado:
		codificação2 = revisado.split(':')[1]
		revisado = revisado.split(':')[0]
	else: codificação2 = 'utf8'
	
	conllu_comparação = open(comparação, 'r', encoding=codificação).read()
	print('As seguintes sentenças, que não foram encontradas em um dos arquivos, serão apagadas na revisão. Continuar?\n')
	print("\n".join(conllu_comparação.split('#!$$')[1:]))
	input('Pressione Enter para continuar...')
	
	conllu_comparação = conllu_comparação.split('#!$$')[0].splitlines()
	novo_conllu = list()
	for i, linha in enumerate(conllu_comparação):
		if not '-->' in linha or len(linha.split('\t')) != 10:
			novo_conllu.append(linha)
		
	open(revisado, 'w', encoding=codificação2).write("\n".join(novo_conllu))
	print('OK!')	
	
if __name__ == '__main__':
    número_de_argumentos_mínimo = 2
    if len(sys.argv) < número_de_argumentos_mínimo + 1:
        print('uso: revisar_UD.py comparação.conllu:utf8 revisado.conllu:utf8')
    elif len(sys.argv) == número_de_argumentos_mínimo + 1:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Argumentos demais')
