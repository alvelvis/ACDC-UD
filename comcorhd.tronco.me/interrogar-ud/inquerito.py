#!/usr/bin/python3
# -*- coding: UTF-8 -*-

print('Content-type:text/html')
print('\n\n')

import functions
from functions import tabela
import cgi,cgitb
cgitb.enable()
import estrutura_dados
import os
from datetime import datetime

arquivos = list()
for i, arquivo in enumerate(os.listdir('conllu')):
	arquivos.append('<option value="'+arquivo+'">'+arquivo+'</option>')

html = open('inquerito.html', 'r').read()
html = html.split('<select name="conllu">')[0] + '<select name="conllu">' + "\n".join(arquivos) + '</select>' + html.split('</select>')[1]

html1 = html.split('<!--SPLIT-->')[0]
html2 = html.split('<!--SPLIT-->')[1]

if os.environ['REQUEST_METHOD'] == 'POST': form = cgi.FieldStorage()

if os.environ['REQUEST_METHOD'] == 'POST' and not 'action' in form.keys():
	ud = form['conllu'].value
	conlluzao = estrutura_dados.LerUD('conllu/' + ud)

	for i, sentence in enumerate(conlluzao):
		sentence2 = sentence
		achou = False
		linhas = list()
		for a, linha in enumerate(sentence2):
			if isinstance(linha, list):
				sentence2[a] = '\t'.join(sentence2[a])
			linhas.append(str(a+1) + ': ' + sentence2[a])
		sentence2 = '\n'.join(sentence2)
		if '# text = ' in form['textheader'].value or '# sent_id = ' in form['textheader'].value:
			form['textheader'].value = form['textheader'].value.split(' = ', 1)[1]
		if '# text = ' + form['textheader'].value in sentence2 or '# sent_id = ' + form['textheader'].value in sentence2:
			html1 += '<h3>' + form['textheader'].value + '</h3><hr><br><form action="inquerito.py?sentnum='+str(i)+'&conllu=' + ud + '&action=alterar" method="POST"><label>Dados do inquérito:<br><div class="tooltip"><input style="display: inline-block;" placeholder="Número da linha" name="token" required><span class="tooltiptextfix" style="max-width:80%">'+'<br>'.join(linhas)+'</span></div> <div style="display: inline-block;" class="tooltip"><input style="display: inline-block;" placeholder="Número da coluna" name="coluna"><span style="display: inline-block;" class="tooltiptext">Caso seja um metadado, não há coluna.<br><br>1: ID | 2: WORD | 3: LEMMA | 4: UPOS | 5: XPOS | 6: FEATS | 7: DEPHEAD | 8: DEPREL | 9: DEPS | 10: MISC</span></div> <input name="valor" placeholder="Novo valor" required> <input style="display: inline-block;" style="display: inline-block;" type="submit" value="Finalizar inquérito"><pre>' + sentence2 + '</pre><input type="hidden" name="textheader" value="' + form['textheader'].value + '"></label></form>'
			achou = True
			break
	if not achou: html1 += 'Sentença não encontrada.'

	html = html1 + html2

elif os.environ['REQUEST_METHOD'] == 'POST' and form['action'].value == 'alterar':
	ud = form['conllu'].value
	conlluzao = estrutura_dados.LerUD('conllu/' + ud)

	data = str(datetime.now()).replace(' ','_').split('.')[0]

	try:
		if isinstance(conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1], list):
			antes = conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1][int(form['coluna'].value)-1]
			conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1][int(form['coluna'].value)-1] = form['valor'].value
		else:
			antes = conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1]
			conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1] = form['valor'].value

		estrutura_dados.EscreverUD(conlluzao, 'conllu/' + ud)

		if not os.path.isfile('inqueritos.txt'):
			open('inqueritos.txt', 'w').write('')

		inqueritos = open('inqueritos.txt', 'r').read()
		open('inqueritos.txt', 'w').write(form['textheader'].value + '\t' + antes + ' --> ' + form['valor'].value + '\t' + form['conllu'].value + '\t' + data + '\n' + inqueritos)

		print('''<head>
				   <meta http-equiv="content-type" content="text/html; charset=UTF-8; width=device-width, initial-scale=1.0"
				     name="viewport">
				 </head>
				 <body><script>window.alert("OK: ''' + antes + ''' --> ''' + form['valor'].value + '''"); window.close();</script></body>''')
		exit()

	except Exception as e:
		print('Erro: ' + str(e))
		exit()

elif os.environ['REQUEST_METHOD'] != 'POST':
	html1 = html.split('<!--SPLIT-->')[0]
	html2 = html.split('<!--SPLIT-->')[1]

	if not os.path.isfile('inqueritos.txt'):
		open('inqueritos.txt', 'w').write('')

	inqueritos = open('inqueritos.txt', 'r').read()
	for linha in inqueritos.splitlines():
		if linha.strip() != '':
			html1 += '<div class="container"><p>' + linha.split('\t')[0] + '</p><p>' + linha.split('\t')[1] + '</p><p>' + linha.split('\t')[2] + '</p><p>' + linha.split('\t')[3] + '</p></div>'

	html = html1 + html2

print(html)
