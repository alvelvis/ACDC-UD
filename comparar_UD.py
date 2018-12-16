# -*- coding: utf-8 -*-

import sys

#Retira os itens de informação, do tipo "# id_sent", mantendo apenas as linhas com "# text" e os tokens em si
#O UD já precisa estar "sentence segmented"
def sem_info(ud_sent_segmented):
	for i, sentença in enumerate(ud_sent_segmented): ud_sent_segmented[i] = [x for x in sentença if not '# ' in x or '# text =' in x]

	return ud_sent_segmented

#Compara arquivos UD, mantendo ou não as informações de cada sentença (id_sent etc.)
def compara(files_list, UD, colunas):
	novotexto = list()
	solitários = dict()
	for arquivo in files_list[1:]:
		solitários[arquivo] = list()

	#Separa cada sentença nos arquivos UD
	for arquivo in files_list:
		UD[arquivo] = UD[arquivo].split('\n\n')
		for i, sentença in enumerate(UD[arquivo]):
			UD[arquivo][i] = UD[arquivo][i].splitlines()

	#Retira os itens de informação, do tipo "# id_sent", mantendo apenas as linhas com "# text" e os tokens em si
	for arquivo in files_list:
		UD[arquivo] = sem_info(UD[arquivo])

	#Início da comparação com o 1º ARQUIVO APENAS
	for sentença in UD[files_list[0]]: #Para cada sentença do arquivo 1
		for a, linha in enumerate(sentença): #Para cada linha nessa sentença
			novotexto.append(linha)
			if '# text = ' in linha: #Se tiver "# text" nessa linha
				text_header = linha
			if '\t' in linha:
				for arquivo in files_list[1:]:
					for subsentença in UD[arquivo]:
						sentença_correta = False
						for b, sublinha in enumerate(subsentença):
							if sublinha == text_header and len(subsentença) == len(sentença):
								sentença_correta = True
							if sentença_correta and a == b:
								for coluna in colunas:
									if sublinha.split('\t')[coluna-1] != linha.split('\t')[coluna-1]:
										novotexto.append('-->[' + str(files_list.index(arquivo) +1) + ']\t' + sublinha.split('\t', 1)[1])
										break
		novotexto.append('')

	#sentenças que têm em um arquivo e não no 1
	for arquivo in files_list[1:]:
		for sentença in UD[arquivo]:
			for linha in sentença:
				if '# text =' in linha:
					tem = False
					for sentença_master in UD[files_list[0]]:
						if linha in sentença_master and len(sentença_master) == len(sentença): tem = True
					if not tem: solitários[arquivo].append(linha)

	solitários_texto = list()
	for solitário in solitários:
		solitários_texto.append('#!$$ Sentenças de "' + solitário + '" [' + str(files_list.index(solitário) +1) + '] que não foram encontradas em "' + files_list[0] + '" ou que apresentavam tokenização diferente:')
		solitários_texto.append('')
		for item in solitários[solitário]:
			solitários_texto.append(item)
		solitários_texto.append('')

	return "\n".join(novotexto) + '\n' + '\n'.join(solitários_texto)

def main(saída, arquivos):
	#Checa os parâmetros
	files_list = list()
	codificação = dict()
	parâmetros = '--' + arquivos.split('--')[1]
	arquivos = arquivos.split('--')[0]
	for arquivo in arquivos.split('!@#'):
		if arquivo.replace('!@#','').strip() != '':
			if ':' in arquivo:
				arquivo_nome = arquivo.split(':')[0]
				codificação[arquivo_nome] = arquivo.split(':')[1]
			else:
				arquivo_nome = arquivo
				codificação[arquivo_nome] = 'utf8'
			files_list.append(arquivo_nome)

	if ':' in saída:
		codificação3 = saída.split(':')[1]
		saída = saída.split(':')[0]
	else:
	    codificação_saída = 'utf8'

	if '--colunas' in parâmetros:
		colunas = parâmetros.split('--colunas!@#')[1].split('!@#')[0].split('#')
		for i in range(len(colunas)):
			colunas[i] = int(colunas[i])
	else: colunas = [1,2,3,4,5,6,7,8,9,10]

	#Abre os arquivos CONLLU e salva o arquivo comparado
	UD = dict()
	for arquivo in files_list:
		UD[arquivo] = open(arquivo, 'r', encoding=codificação[arquivo]).read()

	#Cria cabeçalho
	cabeçalho = files_list[0]
	for i, arquivo in enumerate(files_list[1:]):
		cabeçalho += '\n-->[' + str(i +2) + ']\t' + arquivo
	cabeçalho = 'Colunas: ' + str(colunas) + '\n' + cabeçalho + '\n\n'

	open(saída, 'w', encoding=codificação_saída).write(cabeçalho + compara(files_list, UD, colunas))

if __name__ == "__main__":
	#Atualizar repositório
	if len(sys.argv) == 2 and sys.argv[1] == '--atualizar':
		import atualizar_repo
		atualizar_repo.atualizar()
		print('Atualizado com sucesso!')
		exit()

	#Checa os argumentos
	if len(sys.argv) < 4:
		print("uso: comparar_UD.py saída.conllu:utf8 ud1.conllu:utf8 ud2.conllu:utf8 ... udX.conllu:utf8 <parâmetros>")
		print('O arquivo ud1.conllu será o mais importante, sendo os demais arquivos UD representados apenas se houver discrepâncias, com setas "-->"')
		print('Caso deseje comparar apenas algumas colunas, adicione o parâmetro "--colunas" ao final seguido das colunas que deseja comparar entre "#". Ex: --colunas 2#4#5')
	elif len(sys.argv) >= 4:
		main(sys.argv[1], "!@#".join(sys.argv[2:]))
		print('OK!')
