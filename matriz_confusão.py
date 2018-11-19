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

def get_list(conllu1, conllu2, coluna):
        lista_coluna1 = list()
        lista_coluna2 = list()
        solitários1 = list()
        solitários2 = list()

        #Sentença por sentença do conllu1
        for sentença in conllu1:
                sentença_length = 0
                for linha in sentença:
                        #Encontrou o text_header da sentença
                        if '# text = ' in linha:
                                text_header = linha
                        #Cresce o tamanho de tokens da sentença
                        if isinstance(linha, list):
                                sentença_length += 1
                #Começa a alinhar com o conllu2 para ver se a sentença também tem lá
                tem = False
                for subsentença in conllu2:
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
                                for sublinha in subsentença:
                                    if isinstance(sublinha, list):
                                        lista_coluna2.append(sublinha[coluna-1])
                #Se encontrou sentença igual em conllu2, append!
                if tem:
                        for linha in sentença:
                                if isinstance(linha, list):
                                        lista_coluna1.append(linha[coluna-1])
                #Se não encontrou, solitários.append
                else:
                        solitários1.append(text_header)

        #Procurar os solitários2
        for sentença in conllu2:
                sentença_length = 0
                for linha in sentença:
                        if '# text =' in linha:
                                text_header = linha
                        if isinstance(linha, list):
                                sentença_length += 1
                tem = False
                for subsentença in conllu1:
                        sentença_correta = False
                        subsentença_length = 0
                        for sublinha in subsentença:
                                if sublinha == text_header:
                                        sentença_correta = True
                                if sentença_correta and isinstance(sublinha, list):
                                        subsentença_length += 1
                        if sentença_correta and subsentença_length == sentença_length:
                                tem = True
                if not tem:
                        solitários2.append(text_header)

        return {'matriz_1': lista_coluna1, 'matriz_2': lista_coluna2, 'solitários_1': solitários1, 'solitários_2': solitários2}

def relatório(lista_conllu1, lista_conllu2, conllu1, conllu2, coluna):
                
        
        return 'oi'

def main(ud1, ud2, output, coluna):
	conllu1 = LerUD(ud1)
	conllu2 = LerUD(ud2)
	lista_conllu = get_list(conllu1, conllu2, coluna)
	lista_conllu1 = lista_conllu['matriz_1']
	lista_conllu2 = lista_conllu['matriz_2']
	#pd.options.display.max_rows = 1000
	#pd.options.display.max_columns = 1000
	saída = list()
	saída.append('Col ' + str(coluna)+': ' + feats[coluna])
	saída.append('UD[1]: ' + ud1)
	saída.append('UD[2]: ' + ud2 + '\n')
	saída.append(str(pd.crosstab(pd.Series(lista_conllu1), pd.Series(lista_conllu2), rownames=['UD[1]'], colnames=['UD[2]'], margins=True)))
	saída.append('\n')
	saída.append('#!$$ Sentenças em UD[1] que não foram encontradas em UD[2]:\n')
	for item in lista_conllu['solitários_1']:
	        saída.append(item)
	saída.append('\n#!$$ Sentenças em UD[2] que não foram encontradas em UD[1]:\n')
	for item in lista_conllu['solitários_2']:
	        saída.append(item)

	erros = relatório(listaconllu1, listaconllu2, conllu1, conllu2, coluna)
        saída.append('\n')

        #Output
	if ':' in output: codificação_saída = output.split(':')[1]
	else: codificação_saída = 'utf8'
	output = output.split(':')[0]

	open(output, 'w', encoding=codificação_saída).write("\n".join(saída))

if __name__ == '__main__':
    número_de_argumentos_mínimo = 4

    if len(sys.argv) < número_de_argumentos_mínimo +1:
        print('uso: matriz_confusão.py ud1.conllu:utf8 ud2.conllu:utf8 saída.txt:utf8 coluna')
        print('Colunas:')
        for i in range(len(feats)):
                print(str(i+1) + ': ' + feats[i+1])
    elif len(sys.argv) >= número_de_argumentos_mínimo +1:
        main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    else:
        print('Argumentos demais')
