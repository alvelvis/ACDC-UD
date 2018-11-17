# -*- coding: utf-8 -*-

import sys
from comparar_UD import sem_info

def main(CONLLU_input, CONLLU_output):
    if ':' in CONLLU_input:
        codificação = CONLLU_input.split(':')[1]
        CONLLU_input = CONLLU_input.split(':')[0]
    else: codificação = 'utf8'

    if ':' in CONLLU_output:
        codificação2 = CONLLU_output.split(':')[1]
        CONLLU_output = CONLLU_output.split(':')[0]
    else: codificação2 = 'utf8'

    arquivo_novo = open(CONLLU_input, 'r', encoding=codificação).read().split('\n\n')
    arquivo_novo = [x.splitlines() for x in arquivo_novo if x]
    arquivo_novo = sem_info(arquivo_novo)

    for i, sentença in enumerate(arquivo_novo):
        arquivo_novo[i] = "\n".join(arquivo_novo[i])

    open(CONLLU_output, 'w', encoding=codificação2).write("\n\n".join(arquivo_novo))

    print('OK!')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('uso: apenas_tokens.py ud.conllu:utf8 saída.conllu:utf8')
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Argumentos demais')
