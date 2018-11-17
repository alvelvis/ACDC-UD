# -*- coding: utf-8 -*-

import sys

#Retira os itens de informação, do tipo "# id_sent", mantendo apenas as linhas com "# text" e os tokens em si
#O UD já precisa estar "sentence segmented"
def sem_info(ud_sent_segmented):
	for i, sentença in enumerate(ud_sent_segmented): ud_sent_segmented[i] = [x for x in sentença if not '# ' in x or '# text =' in x]

	return ud_sent_segmented

#Compara 2 arquivos UD, mantendo ou não as informações de cada sentença (id_sent etc.)
def compara(arquivo, arquivo2, texto, texto2, info):
	novotexto = list()

	#Separa cada sentença no arquivo 1 e arquivo 2
	texto = texto.split('\n\n')
	texto2 = texto2.split('\n\n')

	#Tira os itens em branco das listas
	texto = [x.splitlines() for x in texto if x]
	texto2 = [x.splitlines() for x in texto2 if x]

	#Retira os itens de informação, do tipo "# id_sent", mantendo apenas as linhas com "# text" e os tokens em si
	if not info:
		texto = sem_info(texto)
		texto2 = sem_info(texto2)

	#Início da comparação
	for sentença in texto: #Para cada sentença do arquivo 1
		for linha in sentença: #Para cada linha nessa sentença
			if '# text' in linha: #Se tiver "# text" nessa linha
				for sentença2 in texto2: #Início da comparação com o arquivo 2
					for linha2 in sentença2:
						if linha2 == linha: #Alinhou o "# text" do arquivo 1 com o "# text" do arquivo 2
							if sentença != sentença2: #Se a sentença do arquivo1 for diferente da sentença do arquivo 2 (ou seja, houver discrepância em algum token)
								for a, line in enumerate(sentença):
									for b, line2 in enumerate(sentença2):
										if a == b and line == line2: #Alinha os tokens que estão iguais, então printa 1 vez só
											novotexto.append(line)
											break
										elif a == b: #Alinha os tokens que estão diferentes e printa o mesmo token dos arquivos 1 e 2
											novotexto.append(line + '\n--> ' + line2)
											break
								novotexto.append('')
							else: break

	return "\n".join(novotexto)

def main(arquivo, arquivo2, saída, opcionais = ''):
	#Checa os parâmetros
	if ':' in arquivo:
		codificação = arquivo.split(':')[1]
		arquivo = arquivo.split(':')[0]
	else:
		codificação = 'utf8'
		
	if ':' in arquivo2:
		codificação2 = arquivo2.split(':')[1]
		arquivo2 = arquivo2.split(':')[0]
	else:
		codificação2 = 'utf8'
		
	if ':' in saída:
		codificação3 = saída.split(':')[1]
		saída = saída.split(':')[0]
	else:
	    codificação3 = 'utf8'

	if '--com-info' in opcionais: info = True
	else: info = False

	#Abre os arquivos CONLLU e salva o arquivo comparado
	texto = open(arquivo, 'r', encoding=codificação).read()
	texto2 = open(arquivo2, 'r', encoding=codificação2).read()
	open(saída, 'w', encoding=codificação3).write(arquivo + '\n--> ' + arquivo2 + '\n\n' + compara(arquivo, arquivo2, texto, texto2, info))

if __name__ == "__main__":
	#Atualizar repositório
	if len(sys.argv) == 2 and sys.argv[1] == '--atualizar':
		import atualizar_repo
		atualizar_repo.atualizar()
		print('Atualizado com sucesso!')
		exit()
	
	#Checa os argumentos
	if len(sys.argv) < 4:
		print("uso: comparar_UD.py ud1.conllu:utf8 ud2.conllu:utf8 saída.txt:utf8 --com-info")
	elif len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
		print('OK!')
	elif len(sys.argv) == 4 or len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
		print('OK!')
	else:
	    print('Argumentos demais')

