# -*- coding: UTF-8 -*-
import estrutura_dados
import re

#Crio a função que vai ser chamada seja pelo HTML ou seja pelo terminal
def main(arquivoUD, criterio, parametros):

	#Lê o arquivo UD
	qualquercoisa = estrutura_dados.LerUD(arquivoUD)

	#Cria a lista que vai ser enviada seja ao terminal ou ao HTML
	output = list()

	if criterio == 2:
		for a, sentence in enumerate(qualquercoisa):
			sentence2 = sentence
			for b, linha in enumerate(sentence):
				linha2 = linha
				if isinstance(linha2, list):
					sentence2[b] = "\t".join(sentence2[b])
			sentence2 = "\n".join(sentence2)
			if re.search(parametros, sentence2):
				output.append(sentence)

	#If critério 1
	if criterio == 1:

		#Variáveis
		y = parametros.split('#')[0]
		z = int(parametros.split('#')[1])
		k = parametros.split('#')[2]
		w = int(parametros.split('#')[3])

		for sentence in qualquercoisa:
			achei = 'nãoachei'
			descarta = False
			for linha in sentence:
				if isinstance(linha, list): #string != list
					if y in linha[z-1]: #==
						achei = linha[0]
			if achei != 'nãoachei':
				for linha in sentence:
					if isinstance(linha, list): #string != list
						if achei in linha[z-2] and k in linha[z-1]: #Z-2: atenção
							descarta = True
				if descarta == False:
					output.append(sentence)

	#Transforma o output em lista de sentenças (sem splitlines e sem split no \t)
	for a, sentence in enumerate(output):
		for b, linha in enumerate(sentence):
			if isinstance(linha, list):
				sentence[b] = "\t".join(sentence[b])
		output[a] = "\n".join(sentence)

	return output

#Ele só pede os inputs se o script for executado pelo terminal. Caso contrário (no caso do código ser chamado por uma página html), ele não pede os inputs, pois já vou dar a ele os parâmetros por meio da página web
if __name__ == '__main__':
	arquivoUD= input('arraste arquivo:\n').replace("'","")
	qualquercoisa = estrutura_dados.LerUD(arquivoUD)
	criterio=int(input('qual criterio de procura?'))
	while criterio > 2:
	    print('em desenvolvimento')
	    criterio=int(input('qual criterio de procura?'))

	if criterio == 2:
		parametros = input('Expressão regular:\n')

	if criterio == 1:
		y=input('Se um token X marcado como: ')
		z=int(input('Na coluna: '))
		k=input('e nenhum outro token com valor: ')
		w=int(input('na coluna: '))
		nome=input('nomeie sua criação:\n')
		parametros  = y + '#' + str(z) + '#' + k + '#' + str(w)

	#Chama a função principal e printo o resultado, dando a ela os parâmetros dos inputs
	print(main(arquivoUD, criterio, parametros))















