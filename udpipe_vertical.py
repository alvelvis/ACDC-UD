# -*- coding: utf-8 -*-

import sys
from subprocess import call
import os

#Busca no arquivo "com_text" as entradas de texto e tenta alinhar as sentenças
def adiciona_text(arquivo, tokenizado):
    novoarquivo = "\n".join([x for x in arquivo.splitlines() if not x.strip().startswith("# ")])
    novoarquivo = [x for x in novoarquivo.split('\n\n') if x.strip()]
    tokenizado = [x for x in tokenizado.split('\n\n') if x.strip()]
    
    for i, sentença in enumerate(novoarquivo):
        for linha in tokenizado[i].splitlines():
            if linha.strip().startswith('# '):
                novoarquivo[i] = linha + '\n' + novoarquivo[i]

    for i, sentença in enumerate(novoarquivo):
        novoarquivo[i] = novoarquivo[i].splitlines()
        headerDifference = len([x for x in novoarquivo[i] if "# " in x]) - len([x for x in tokenizado[i].splitlines() if "# " in x])
        for a, linha in enumerate(tokenizado[i].splitlines()):
            if '\t' in linha and '-=' in linha.split('\t')[0]:
                novoarquivo[i].insert(a + headerDifference, linha.split('\t')[0].split('-=')[0] + '\t' + linha.split('\t')[0].split('-=')[1] + '\t_\t_\t_\t_\t_\t_\t_\t_')
        novoarquivo[i] = "\n".join(novoarquivo[i])

    #Linha em branco no final
    return "\n\n".join(novoarquivo) + '\n\n'

#Apaga o "# text" E as MWES
def apagar_text(arquivo):
    arquivo = arquivo.splitlines()
    novo_arquivo = list()
    for i, linha in enumerate(arquivo):
        #Retira as hashtags e as MWES
        if '\t' in linha and not '-=' in linha.split('\t')[0]:
            novo_arquivo.append(linha)
        elif linha.strip() == '':
            novo_arquivo.append('')

    return '\n'.join(novo_arquivo)

def main(modelo, tokenizado, resultado):

    try:
        com_text = open(tokenizado, 'r').read()
    except:
        com_text = open(tokenizado, 'r', encoding="latin-1").read()
    open(tokenizado + 'x', 'w').write(apagar_text(com_text))

    #Chama o udpipe
    call('yes "\n" | ./udpipe-* --tag --parse --input vertical "' + modelo + '" "' + tokenizado + 'x" > "' + resultado + '"', shell=True)

    #Apaga o arquivo temporário "sem_text" (e sem MWE)
    os.remove(tokenizado + 'x')

    novo_texto = adiciona_text(open(resultado, 'r').read(), com_text)
    open(resultado, 'w').write(novo_texto)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('uso: udpipe_vertical.py modelo.udpipe tokenizado.conllu resultado.conllu')
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('Argumentos demais')
