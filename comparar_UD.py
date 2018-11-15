# -*- coding: utf-8 -*-

import sys

def compara(arquivo, arquivo2, texto, texto2, info):
	novotexto = list()
	texto = texto.split('\n\n')
	texto2 = texto2.split('\n\n')
	texto = [x.splitlines() for x in texto if x]
	texto2 = [x.splitlines() for x in texto2 if x]
	
	if not info:
		for i, sentença in enumerate(texto): texto[i] = [x for x in sentença if not '# ' in x or '# text =' in x]
		for i, sentença in enumerate(texto2): texto2[i] = [x for x in sentença if not '# ' in x or '# text =' in x]

	for sentença in texto:
		for linha in sentença:
			if '# text' in linha:
				for sentença2 in texto2:
					for linha2 in sentença2:
						if linha2 == linha:
							if sentença != sentença2:
								for a, line in enumerate(sentença):
									for b, line2 in enumerate(sentença2):
										if a == b and line == line2:
											novotexto.append(line)
											break
										elif a == b:
											novotexto.append('--> ' + line + ' #' + line2)
											break
								novotexto.append('')
							else: break

	return "\n".join(novotexto)

def main(arquivo, arquivo2, saída, opcionais = ''):
	if '--cod-1' in opcionais: codificação = opcionais.split('--cod-1')[1].split('--')[0].strip()
	else: codificação = 'utf8'
	if '--cod-2' in opcionais: codificação2 = opcionais.split('--cod-2')[1].split('--')[0].strip()
	else: codificação2 = 'utf8'
	if '--cod-3' in opcionais: codificação3 = opcionais.split('--cod-3')[1].split('--')[0].strip()
	else: codificação3 = 'utf8'
	if '--sem-info' in opcionais: info = False
	else: info = True

	texto = open(arquivo, 'r', encoding=codificação).read()
	texto2 = open(arquivo2, 'r', encoding=codificação2).read()
	open(saída, 'w', encoding=codificação3).write(arquivo + '\n' + arquivo2 + '\n\n' + compara(arquivo, arquivo2, texto, texto2, info))

if __name__ == "__main__":
	#atualizar
	if len(sys.argv) == 2 and sys.argv[1] == '--atualizar':
		import atualizar
		atualizar.atualizar()
		print('Atualizado com sucesso!')
		exit()
	if len(sys.argv) < 4:
		print("uso: comparar.py --atualizar conllu1 conllu2 saída.txt --cod-1 --cod-2 --cod-3 --sem-info")
	elif len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
		print('OK!')
	elif len(sys.argv) > 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
		print('OK!')

