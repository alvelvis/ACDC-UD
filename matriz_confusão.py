# -*- coding: utf-8 -*-

import sys
from estrutura_dados import LerUD

try:
        import pandas as pd
except:
        try:
                from pip import main as pipmain
        except:
                print('Instale a biblioteca "pandas" e tente novamente.')
                exit()
        else:
                pipmain(['install', 'pandas'])
                print('Biblioteca "pandas" instalada com sucesso!')
                exit()

feats = {
                1: "ID",
                2: "FORM",
                3: "LEMMA",
                4: "UPOSTAG",
                5: "XPOSTAS",
                6: "FEATS",
                7: "HEAD",
                8: "DEPREL",
                9: "DEPS",
                10: "MISC",
}

def get_list(conllu, coluna, conllu2):
        lista_coluna = list()
        solitários = list()

        #Sentença por sentença do conllu1
        for a, sentença in enumerate(conllu):
                sentença_length = 0
                for i, linha in enumerate(sentença):
                        #Encontrou o text_header da sentença
                        if '# text = ' in linha:
                                text_header = linha
                        #Cresce o tamanho de tokens da sentença
                        if isinstance(linha, list):
                                sentença_length += 1
                #Começa a alinhar com o conllu2 para ver se a sentença também tem lá
                for subsentença in conllu2:
                        tem = False
                        sentença_correta = False
                        subsentença_length = 0
                        for sublinha in subsentença:
                                #Encontrou a sentença cujo text_header é igual
                                if sublinha == text_header:
                                        sentença_correta = True
                                #Cresceu o tamanho de tokens da sentença correta
                                if sentença_correta and isinstance(sublinha, list):
                                        subsentença_length += 1
                        #Se tiver uma sentença igual em text_header e em tamanho, tem = True
                        if sentença_correta and subsentença_length == sentença_length:
                                tem = True
                                break
                #Se encontrou sentença igual em conllu2, append!
                if tem:
                        for linha in sentença:
                                if isinstance(linha, list):
                                        lista_coluna.append(linha[coluna-1])
                #Se não encontrou, solitários.append
                else:
                        solitários.append(text_header)

        return {'matriz': lista_coluna, 'solitários': solitários}

def main(ud1, ud2, coluna):
	conllu1 = LerUD(ud1)
	conllu2 = LerUD(ud2)
	lista_conllu1 = get_list(conllu1, coluna, conllu2)
	lista_conllu2 = get_list(conllu2, coluna, conllu1)
	#pd.options.display.max_rows = 1000
	#pd.options.display.max_columns = 1000
	print('Col ' + str(coluna)+': ' + feats[coluna])
	print('UD[1]: ' + ud1)
	print('UD[2]: ' + ud2 + '\n')
	print(pd.crosstab(pd.Series(lista_conllu1['matriz']), pd.Series(lista_conllu2['matriz']), rownames=['UD[1]'], colnames=['UD[2]'], margins=True))
	print('')
	print('#!$$ Sentenças em UD[1] que não foram encontradas em UD[2]:\n')
	for item in lista_conllu1['solitários']:
	        print(item)
	print('\n#!$$ Sentenças em UD[2] que não foram encontradas em UD[1]:\n')
	for item in lista_conllu2['solitários']:
	        print(item)
	print('')

if __name__ == '__main__':
    número_de_argumentos_mínimo = 3

    if len(sys.argv) < número_de_argumentos_mínimo +1:
        print('uso: matriz_confusão.py ud1.conllu:utf8 ud2.conllu:utf8 coluna')
        print('Colunas:')
        for i in range(len(feats)):
                print(str(i+1) + ': ' + feats[i+1])
    elif len(sys.argv) >= número_de_argumentos_mínimo +1:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    else:
        print('Argumentos demais')
