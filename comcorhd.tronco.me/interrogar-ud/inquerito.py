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
import re

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

	html1 = html1.split('<div class="header">')[0] + '<div class="header"><h1>Novo inquérito</h1><br><br>' + ud + '</div>' + html1.split('</div>', 2)[2]

	for i, sentence in enumerate(conlluzao):
		sentence2 = sentence
		achou = False
		#linhas = list()
		for a, linha in enumerate(sentence2):
			if isinstance(linha, list):
				sentence2[a] = '\t'.join(sentence2[a])
			#linhas.append(str(a+1) + ': ' + sentence2[a])
		sentence2 = '\n'.join(sentence2)
		if '# text = ' in form['textheader'].value or '# sent_id = ' in form['textheader'].value:
			form['textheader'].value = form['textheader'].value.split(' = ', 1)[1]
		if '# text = ' + form['textheader'].value + '\n' in sentence2 or '# sent_id = ' + form['textheader'].value + '\n' in sentence2:
			html1 += '<h3><a style="color:black" id="HEADER">' + form['textheader'].value + '</a></h3><hr><br><form action="inquerito.py?sentnum='+str(i)+'&conllu=' + ud + '&action=alterar" method="POST"><label>Dados do inquérito:<br><div class="tooltip"><input style="display: inline-block;" placeholder="Número da linha" id="token" name="token" required><span class="tooltiptext">Clique na linha/coluna que deseja alterar.</span></div> <div style="display: inline-block;" class="tooltip"><input style="display: inline-block;" placeholder="Número da coluna" id="coluna" name="coluna"><span style="display: inline-block;" class="tooltiptext">Caso seja um metadado, não há coluna.<br><br>1: ID | 2: WORD | 3: LEMMA | 4: UPOS | 5: XPOS | 6: FEATS | 7: DEPHEAD | 8: DEPREL | 9: DEPS | 10: MISC</span></div> > <div class="tooltip"><input name="valor" id="valor" placeholder="Novo valor" required><span class="tooltiptext">Valor para o qual a linha/coluna será substituída.</span></div> <input style="display: inline-block;" style="display: inline-block;" type="submit" value="Finalizar inquérito"><pre>'

			for a, linha in enumerate(sentence2.splitlines()):
				if not '\t' in linha:
					html1 += '''<a style="cursor:pointer; color:white;" onclick="document.getElementById('valor').value = ' ''' + linha + ''' '; document.getElementById('token').value = ' ''' + str(a+1) + ''' '; document.getElementById('coluna').value = ''; $('valor').focus(); ">''' + linha + '</a>'
				else:
					for b, coluna in enumerate(linha.split('\t')):
						html1 += '''<a style="cursor:pointer; color:white;" onclick="document.getElementById('valor').value = ' ''' + coluna + ''' '; document.getElementById('token').value = ' ''' + str(a+1) + ''' '; document.getElementById('coluna').value = ' ''' + str(b+1) + ''' '; $('valor').focus(); ">''' + coluna + '</a>&#9;'
				html1 += '<br>'

			html1 += '</pre><input type="hidden" name="textheader" value="' + form['textheader'].value + '"></label></form>'
			achou = True
			break
	if not achou: html1 += 'Sentença não encontrada.'

	html = html1 + html2

elif os.environ['REQUEST_METHOD'] == 'POST' and form['action'].value == 'alterar':
	ud = form['conllu'].value
	conlluzao = estrutura_dados.LerUD('conllu/' + ud)
	form['token'].value = form['token'].value.strip()
	form['coluna'].value = form['coluna'].value.strip()
	form['valor'].value = form['valor'].value.strip()
	data = str(datetime.now()).replace(' ','_').split('.')[0]

	try:
		if isinstance(conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1], list):
			antes = '\t'.join(conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1])
			conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1][int(form['coluna'].value)-1] = form['valor'].value
			depois = '\t'.join(conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1])
		else:
			antes = conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1]
			conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1] = form['valor'].value
			depois = conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1]

		estrutura_dados.EscreverUD(conlluzao, 'conllu/' + ud)

		if not os.path.isfile('inqueritos.txt'):
			open('inqueritos.txt', 'w').write('')

		inqueritos = open('inqueritos.txt', 'r').read()
		open('inqueritos.txt', 'w').write(form['textheader'].value + '!@#' + antes + ' --> ' + depois + '!@#' + form['conllu'].value + '!@#' + data + '\n' + inqueritos)

		print('''<head>
				   <meta http-equiv="content-type" content="text/html; charset=UTF-8; width=device-width, initial-scale=1.0" name="viewport">
				 </head>
				 <body><script>window.alert("ANTES:\\n''' + antes + '''\\n\\nDEPOIS:\\n''' + depois + '''"); window.close();</script></body>''')

	except Exception as e:
		print('Erro: ' + str(e))
		exit()

elif os.environ['REQUEST_METHOD'] != 'POST':

	if not os.path.isfile('inqueritos.txt'):
		open('inqueritos.txt', 'w').write('')

	inqueritos = open('inqueritos.txt', 'r').read()
	for a, linha in enumerate(inqueritos.splitlines()):
		if linha.strip() != '':
			html1 += '<div class="container"><form id="form_' + str(a) + '" action="inquerito.py" method="POST"><input name="textheader" type="hidden" value="' + linha.split('!@#')[0] + '"><input name="conllu" type="hidden" value="' + linha.split('!@#')[2] + '"><p><h3><a href="#" onclick="form_' + str(a) + '.submit()">' + linha.split('!@#')[0] + '</a></h3></p><p>ANTES: ' + linha.split('!@#')[1].split(' --> ')[0] + '</p><p>DEPOIS: ' + linha.split('!@#')[1].split(' --> ')[1] + '</p><small><p>' + linha.split('!@#')[2] + '</p><p>' + linha.split('!@#')[3] + '</p></small></form></div>'

	html = html1 + html2

print(html)
