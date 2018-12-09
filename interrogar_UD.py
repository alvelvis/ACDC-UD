# -*- coding: UTF-8 -*-
import estrutura_dados
import re

#Crio a função que vai ser chamada seja pelo HTML ou seja pelo terminal
def main(arquivoUD, criterio, parametros):

	#Lê o arquivo UD
	qualquercoisa = estrutura_dados.LerUD(arquivoUD)

	#Cria a lista que vai ser enviada seja ao terminal ou ao HTML
	output = list()

	#Regex
	if criterio == 1:
		for a, sentence in enumerate(qualquercoisa):
			sentence2 = sentence
			for b, linha in enumerate(sentence):
				linha2 = linha
				if isinstance(linha2, list):
					sentence2[b] = "\t".join(sentence2[b])
			sentence2 = "\n".join(sentence2)
			regex = re.search(parametros, sentence2, flags=re.IGNORECASE|re.MULTILINE)
			if regex:
				new_sentence = re.sub('(' + parametros + ')', r'<b>\1</b>', sentence2, flags=re.IGNORECASE|re.MULTILINE)
				tokens = list()
				header = '!@#'
				for linha in new_sentence.splitlines():
					if '# text = ' in linha:
						header = linha
					if 'b>' in linha and '\t' in linha:
						tokens.append(linha.split('\t')[1].replace('<b>','').replace('</b>',''))
				header2 = header
				for token in tokens:
					header2 = header2.replace(token, '<b>' + token + '</b>')
				new_sentence = new_sentence.replace(header, header2)
				output.append(new_sentence.splitlines())

	#If critério 2
	if criterio == 2:

		#Variáveis
		y = parametros.split('#')[0]
		z = int(parametros.split('#')[1])
		k = parametros.split('#')[2].split('|')
		w = int(parametros.split('#')[3])

		for sentence in qualquercoisa:
			achei = 'nãoachei'
			descarta = False
			for i, linha in enumerate(sentence):
				if isinstance(linha, list):
					if y == linha[z-1]:
						achei = linha[0]
						token = linha[1]
						sentence[i]='<b>'+'\t'.join(sentence[i])+'</b>'
						sentence[i]=sentence[i].split('\t')
						break
			for i, linha in enumerate(sentence):
				if '# text' in linha:
					sentence[i]= sentence[i].replace(token, '<b>'+token+'</b>')

			if achei != 'nãoachei':
				for linha in sentence:
					if isinstance(linha, list):
						for k_subitem in k:
							if achei == linha[6] and k_subitem == linha[z-1]:
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

	if criterio == 1:
		parametros = input('Expressão regular:\n')

	if criterio == 2:
		y=input('Se um token X marcado como: ')
		z=int(input('Na coluna: '))
		k=input('e nenhum outro token com valor: ')
		w=int(input('na coluna: '))
		nome=input('nomeie sua criação:\n')
		parametros  = y + '#' + str(z) + '#' + k + '#' + str(w)

	#Chama a função principal e printo o resultado, dando a ela os parâmetros dos inputs
	print(main(arquivoUD, criterio, parametros))















