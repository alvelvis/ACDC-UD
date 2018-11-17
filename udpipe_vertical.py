# -*- coding: utf-8 -*-

import sys
import os

def adiciona_text(arquivo):
    novoarquivo = arquivo.split('\n\n')
    for i, sentença in enumerate(novoarquivo):
        text = str()
        tokens = sentença.splitlines()
        for token in tokens:
            text = text + ' ' + token.split('\t')[1]
        novoarquivo[i] = '# text = ' + text.strip() + '\n' + novoarquivo[i]

    return "\n\n".join(novoarquivo)


def main(modelo, tokenizado, resultado):
    os.system('cat | ./udpipe-.* --input vertical --tag --parse ' + modelo + ' ' + tokenizado + ' > ' + resultado)

    open(resultado, 'w').write(adiciona_text(open(resultado, 'r').read()))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('uso: udpipe_vertical modelo.udpipe tokenizado.conllu resultado.conllu')
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('Argumentos demais')
