# -*- coding: utf-8 -*-

import sys
from subprocess import call

def adiciona_text(arquivo, tokenizado):
    novoarquivo = arquivo.split('\n\n')
    novoarquivo = [x for x in novoarquivo if x.strip() != '']
    tokenizado = tokenizado.split('\n\n')

    for i, sentença in enumerate(novoarquivo):
        for linha in tokenizado[i].splitlines():
            if '# text = ' in linha:
                novoarquivo[i] = linha + '\n' + novoarquivo[i]
                break

    return "\n\n".join(novoarquivo) + '\n'

def apagar_text(arquivo):
    arquivo = arquivo.splitlines()
    novo_arquivo = list()
    for i, linha in enumerate(arquivo):
        if not '# text = ' in linha:
            novo_arquivo.append(linha)

    return '\n'.join(novo_arquivo)


def main(modelo, tokenizado, resultado):

    com_text = open(tokenizado, 'r').read()
    open(tokenizado, 'w').write(apagar_text(com_text))
    call('cat | ./udpipe-* --tag --parse --input vertical "' + modelo + '" "' + tokenizado + '" > "' + resultado +'"', shell=True)
    novo_texto = adiciona_text(open(resultado, 'r').read(), com_text)
    open(resultado, 'w').write(novo_texto)
    print('OK!')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('uso: udpipe_vertical.py modelo.udpipe tokenizado.conllu resultado.conllu')
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Argumentos demais')
