# -*- coding: utf-8 -*-

import sys
import os
from subprocess import call

def adiciona_text(arquivo):
    novoarquivo = arquivo.split('\n\n')
    novoarquivo = [x for x in novoarquivo if x]
    for i, sentença in enumerate(novoarquivo):
        text = str()
        tokens = sentença.splitlines()
        for token in tokens:
            if not '# ' in token and not '-' in token.split('\t')[0]:
                text = text + ' ' + token.split('\t')[1]
        novoarquivo[i] = '# text = ' + text.strip() + '\n' + novoarquivo[i]

    return "\n\n".join(novoarquivo)


def main(modelo, tokenizado, resultado):

    call('cat | ./udpipe-* --tag --parse --input vertical "' + modelo + '" "' + tokenizado + '" > "' + resultado +'"', shell=True)
    open(resultado, 'w').write(adiciona_text(open(resultado, 'r').read()))
    print('OK!')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('uso: udpipe_vertical.py modelo.udpipe tokenizado.conllu resultado.conllu')
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Argumentos demais')
