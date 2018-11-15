# -*- coding: utf-8 -*-

import sys
import re

#Retorna uma lista com cada ocorrência do ACDC e dispensa qualquer outra informação
def coletaresultadosACDC(texto):
    texto = re.sub('<i> id.*?</i>:','',texto)
    texto = re.sub('<[bB][rR]>','',texto)
    texto = re.split('<[dDiIvV]',texto)[0]
    texto = re.split(r'<[Hh][Rr]>',texto)[3:]

    #Cria uma outra lista com todos os itens da lista original, porém retirando os espaços (strip) e não adicionando à nova lista os itens vazios (if x)
    texto = [x.strip() for x in texto if x]

    print(len(texto), 'ocorrências de busca no AC/DC')
    return texto

#Retorna uma lista com cada sentença (e tokens em sublista (e colunas em subsub))
def transformaUDemLista(texto):
    texto = texto.split('\n\n')
    texto = [x.splitlines() for x in texto if x]
    for i, sentença in enumerate(texto):
        for k, token in enumerate(sentença):
            texto[i][k] = texto[i][k].split('\t')

    print(len(texto), 'sentenças no arquivo .conllu')
    return texto

#Procura um resultado do ACDC no UD e realiza a substituição
def substituiUD(ud, item, palavranegrito, critério):
    for a, sentença in enumerate(ud):
        for b, linha in enumerate(sentença):

            #Retira as marcas de strong na hora de comparar se é a sentença que quero e o ponto final com espaço
            if '# text = ' + re.sub(r'</?[sS][tT][rR][oO][nN][gG]>','',re.sub(' .$','.',item)) in linha:

                #Identifica a palavra bold no item do ACDC e o número do token no UD
                palavrabold = re.search(r'<[sS][tT][rR][oO][nN][gG]>(.*)</[sS][tT][rR][oO][nN][gG]>', item)[1].split()[palavranegrito]
                for token in sentença:
                    if len(token) == 10 and token[1] == palavrabold:
                        númerodobold = token[0]
                        break

                #Procura por palavras que apontem para a bold e realiza a substituição
                for c, token in enumerate(sentença):
                    if len(token) == 10 and token[6] == númerodobold and token[int(critério.split(':')[0])] == critério.split(':')[1]:
                        ud[a][c][int(critério.split(':')[0])] = ud[a][c][int(critério.split(':')[0])].replace(critério.split(':')[1], critério.split(':')[2])

                #Já fez a mudança em todos os tokens necessários, parar de rodar entre as sentenças
                break

    #Retorna o UD alterado
    return ud

#Função principal
def main(códigofonte, conllu, saída, opcionais = ''):

    #Checa opcionais
    if '--cod-acdc' in opcionais: codificação = opcionais.split('--cod-acdc')[1].split('--')[0].strip()
    else: codificação = 'utf8'
    if '--cod-ud' in opcionais: codificação2 = opcionais.split('--cod-ud')[1].split('--')[0].strip()
    else: codificação2 = 'utf8'
    if '--cod-saída' in opcionais: codificação3 = opcionais.split('--cod-saída')[1].split('--')[0].strip()
    else: codificação3 = 'utf8'
    if '--palavra-negrito' in opcionais: palavranegrito = int(opcionais.split('--palavra-negrito')[1].split('--')[0].strip())
    else: palavranegrito = 0
    if '--critério' in opcionais: critério = opcionais.split('--critério')[1].split('--')[0].strip()
    else: critério = '7:ccomp:ccomp parataxis'
    if not '--não-marcar' in opcionais: critério += '#!$'

    print(códigofonte, conllu, saída, codificação, codificação2, codificação3, str(palavranegrito), critério)

    #Transforma em lista e limpa o código fonte e o conllu
    acdc = coletaresultadosACDC(open(códigofonte, 'r', encoding=codificação).read())
    ud = transformaUDemLista(open(conllu, 'r', encoding=codificação2).read())

    #Chama a substituição para cada item do ACDC
    for i, item in enumerate(acdc):
        ud = substituiUD(ud, item, palavranegrito, critério)
        print('(' + str(i+1) + '/' + str(len(acdc)) + ') ' + item)

    #Salva o arquivo final :) (antes tem que transformar a lista em str)
    for i, sentença in enumerate(ud):
        for k, linha in enumerate(sentença):
            ud[i][k] = "\t".join(linha)
        ud[i] = "\n".join(sentença)
    open(saída, 'w', encoding=codificação3).write('\n\n'.join(ud))

#Checa os argumentos
if __name__ == '__main__':

    #atualizar
    if len(sys.argv) == 2 and sys.argv[1] == '--atualizar':
        import atualizar_repo
        atualizar_repo.atualizar()
        print('Atualizado com sucesso!')
        exit()

    #apenas os argumentos essenciais
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    #argumentos essenciais + opcionais
    elif len(sys.argv) > 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))

    #nem os argumentos essenciais
    else: print('uso: acdc-procura.py --atualizar ACDC.html UD.conllu SAÍDA.conllu <opcionais>'
                + '\n\nOpcionais:'
                + '\n--cod-acdc utf8'
                + '\n--cod-ud utf8'
                + '\n--cod-saída utf8'
                + '\n--palavra-negrito 0 (para casos de negrito com mais de uma palavra)'
                + '\n--critério 7:ccomp:ccomp parataxis (coluna:padrão:substituição)
                + '\n--não-marcar (não marcar as sentenças que foram alteradas)')
