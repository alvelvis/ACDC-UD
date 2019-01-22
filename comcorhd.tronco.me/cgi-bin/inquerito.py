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
import difflib

arquivos = list()
for i, arquivo in enumerate(os.listdir('/interrogar-ud/conllu')):
	arquivos.append('<option value="'+arquivo+'">'+arquivo+'</option>')

html = open('/interrogar-ud/inquerito.html', 'r').read()
html = html.split('<select name="conllu">')[0] + '<select name="conllu">' + "\n".join(arquivos) + '</select>' + html.split('</select>')[1]

html1 = html.split('<!--SPLIT-->')[0]
html2 = html.split('<!--SPLIT-->')[1]

def printar(coluna = '', valor = '', onlysent = False):
	global html
	global html1
	global html2

	html1 += '<form action="/cgi-bin/inquerito.py?action=filtrar" method="POST">Filtrar relatório:<br><select name="coluna" required><option value=":">Tudo</option><option value="6">Etiqueta</option><option value="0"># text</option><option value="7"># sent_id</option><option value="2">CoNLLU</option><option value="3">Data</option><option value="4">Página no Interrogatório</option></select> <input type=text autofocus="true" name=valor value="' + valor + '" required> <input type=submit value="Realizar filtro"  style="display:block-inline">'
	html1 += '<input type=checkbox name=onlysent checked>Apenas sentenças</input>' if onlysent else '<input type=checkbox name=onlysent >Apenas sentenças</input>'

	if coluna: html1 += ' <a style="display:block-inline" class="close-thik" href="/cgi-bin/inquerito.py"></a>'

	html1 += '</form><br><br>'

	if not os.path.isfile('/interrogar-ud/inqueritos.txt'):
		open('/interrogar-ud/inqueritos.txt', 'w').write('')

	html42 = ''
	total = 0
	javistos = list()
	inqueritos = open('/interrogar-ud/inqueritos.txt', 'r').read()
	for a, linha in enumerate(inqueritos.splitlines()):
		if linha.strip() != '':
			if (coluna != ':' and valor and len(linha.split('!@#')) > int(coluna) and (re.search(valor, linha.split('!@#')[int(coluna)], flags=re.I|re.M)) and linha.split('!@#')[int(coluna)] != 'NONE') or (not coluna) or (coluna == ':' and re.search(valor, linha, flags=re.I|re.M)):
				if (not onlysent) or (onlysent and not linha.split('!@#')[0] in javistos):
					html42 += '<div class="container"><form target="_blank" id="form_' + str(a) + '" action="/cgi-bin/inquerito.py" method="POST"><input name="textheader" type="hidden" value="' + linha.split('!@#')[0] + '"><input name="conllu" type="hidden" value="' + linha.split('!@#')[2] + '">'
					if len(linha.split('!@#')) >= 7 and linha.split('!@#')[6] != 'NONE': html42 += '<p><small>#' + linha.split('!@#')[6].replace('<b>','@BOLD').replace('</b>','/BOLD').replace('<','&lt;').replace('>','&gt;').replace('@BOLD', '<b>').replace('/BOLD', '</b>') + '</small></p>'
					html42 += '<p><h3><a style="cursor:pointer" onclick="form_' + str(a) + '.submit()">' + linha.split('!@#')[0] + '</a></h3></p>'
					if len(linha.split('!@#')) >= 8 and linha.split('!@#')[7] != 'NONE': html42 += '<p>sent_id = ' + linha.split('!@#')[7] + '</p><input name="sentid" type="hidden" value="' + linha.split('!@#')[7] + '">'
					if len(linha.split('!@#')) >= 6 and linha.split('!@#')[4] != 'NONE' and linha.split('!@#')[5] != 'NONE': html42 = html42 + '<p>Página no Interrogatório: <a target="_blank" href="' + linha.split('!@#')[5] + '">' + linha.split('!@#')[4].replace('<b>','@BOLD').replace('</b>','/BOLD').replace('<','&lt;').replace('>','&gt;').replace('@BOLD', '<b>').replace('/BOLD', '</b>') + '</a></p>'
					if (not onlysent): html42 += '<pre>ANTES:\t' + linha.split('!@#')[1].split(' --> ')[0].replace('<b>', '@BOLD').replace('</b>','/BOLD').replace('<','&lt;').replace('>','&gt;').replace('@BOLD', '<b>').replace('/BOLD', '</b>') + '</pre><pre>DEPOIS:\t' + linha.split('!@#')[1].split(' --> ')[1].replace('<b>','@BOLD').replace('</b>','/BOLD').replace('<','&lt;').replace('>','&gt;').replace('@BOLD', '<b>').replace('/BOLD', '</b>') + '</pre>'
					html42 += '<small><p>' + linha.split('!@#')[2] + '</p><p>' + linha.split('!@#')[3] + '</p></small></form></div>'
					total += 1
					javistos.append(linha.split('!@#')[0])

	html = html1 + 'Inquéritos: ' + str(total) + '<br><br>' + html42 + html2

if os.environ['REQUEST_METHOD'] == 'POST': form = cgi.FieldStorage()

if os.environ['REQUEST_METHOD'] == 'POST' and (not 'action' in form.keys() or (form['action'].value != 'alterar' and form['action'].value != 'filtrar' )):
	ud = form['conllu'].value
	conlluzao = estrutura_dados.LerUD('/interrogar-ud/conllu/' + ud)
	if 'finalizado' in form: html1 += '<span style="background-color: cyan">Inquérito concluído com sucesso!</span><br><br><br>'

	html1 = html1.split('<div class="header">')[0] + '<div class="header"><h1>Novo inquérito</h1><br><br>' + ud + '<br><br><a href="inquerito.py">Relatório de inquéritos</a></div>' + html1.split('</div>', 2)[2]

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
			html1 += '<form action="inquerito.py?sentnum='+str(i)+'&conllu=' + ud + '&action=alterar" method="POST">'
			if 'sentid' in form: html1 = html1 + '<input type=hidden name=sentid value="' + form['sentid'].value.replace('"', '\"') + '">'
			if 'link_interrogatorio' in form and not 'teste' in form['link_interrogatorio'].value.lower():
				html1 = html1 + '<input type=hidden name=link_interrogatorio value="' + form['link_interrogatorio'].value + '">'
			if 'nome_interrogatorio' in form and not 'teste' in form['nome_interrogatorio'].value.lower():
				html1 = html1 + '<input type=hidden name=nome_interrogatorio value="' + form['nome_interrogatorio'].value + '">'
				if 'occ' in form: html1 += '<input type=hidden name=occ value="' + form['occ'].value + '">'
			html1 += '''Tipo de inquérito:<br><input type="text" placeholder="Crie uma categoria para este tipo de inquérito (opcional)" id=tag name="tag" list="cars" />'''
			html1 += '<script>var x = document.cookie.split("tag=")[1]; if (x && x != "NONE") { document.getElementById("tag").value = x }; </script>'
			html1 += '''<datalist id="cars">'''
			if not os.path.isfile('/interrogar-ud/inqueritos_cars.txt'): open('/interrogar-ud/inqueritos_cars.txt', 'w').write('')
			for linha in open('/interrogar-ud/inqueritos_cars.txt', 'r').read().splitlines():
				if linha:
					html1 += '<option>' + linha.replace('<','&lt;').replace('>','&gt;') + '</option>'
			html1 += '</datalist><br><br>'
			html1 += 'Dados do inquérito:<br><div class="tooltip"><input style="display: inline-block;" placeholder="Número da linha" id="token" name="token" required><span class="tooltiptext">Linha a ser alterada.</span></div> <div style="display: inline-block;" class="tooltip"><input style="display: inline-block;" placeholder="Número da coluna" id="coluna" name="coluna"><span style="display: inline-block;" class="tooltiptext">Coluna a ser alterada.<br>Caso seja um metadado, a linha não é dividida em colunas: deixar em branco.<br><br>1: ID | 2: WORD | 3: LEMMA | 4: UPOS | 5: XPOS | 6: FEATS | 7: DEPHEAD | 8: DEPREL | 9: DEPS | 10: MISC</span></div> > <div class="tooltip" style="width:40%"><input name="valor" list="barradaluisa" id="valor" style="width:100%" placeholder="Novo valor" required>'
			html1 += '<datalist id="barradaluisa">'
			for item in open('/interrogar-ud/novovalor.txt', 'r').read().splitlines():
				html1 += '<option>' + item + '</option>'
			html1 += '</datalist><span class="tooltiptext">Valor para o qual a linha/coluna será substituída.</span></div> <input style="display: inline-block;" type="submit" value="Finalizar inquérito"><br><br><br><b>Clique na linha/coluna que deseja alterar:</b><br><br><div style="block"><table id="t01">'

			for a, linha in enumerate(sentence2.splitlines()):
				if not '\t' in linha:
					html1 += '''<tr><td colspan="42" style="cursor:pointer; color:black;" onclick="document.getElementById('valor').value = \'''' + linha.replace("'","\\'") + '''\'; document.getElementById('token').value = \'''' + str(a+1) + '''\'; document.getElementById('coluna').value = ''; document.getElementById('valor').focus(); topfunction() ">''' + linha + '</td></tr>'
				else:
					html1 += '<tr>'
					for b, coluna in enumerate(linha.split('\t')):
						html1 += '''<td style="cursor:pointer; color:black;" onclick="document.getElementById('valor').value = \'''' + coluna.replace("'","\\'") + '''\'; document.getElementById('token').value = \'''' + str(a+1) + '''\'; document.getElementById('coluna').value = \'''' + str(b+1) + '''\'; document.getElementById('valor').focus(); topfunction()">''' + coluna.replace('<','&lt;').replace('>','&gt;') + '</td>'
					html1 += '</tr>'

			html1 += '</div></table><input type="hidden" name="textheader" value="' + form['textheader'].value + '"></label></form>'
			achou = True
			break
	if not achou: html1 += 'Sentença não encontrada.'

	html = html1 + html2

elif os.environ['REQUEST_METHOD'] == 'POST' and form['action'].value == 'alterar':
	ud = form['conllu'].value
	if 'nome_interrogatorio' in form: nome = form['nome_interrogatorio'].value
	else: nome = ''
	if 'link_interrogatorio' in form: link = form['link_interrogatorio'].value
	else: link = ''
	if 'sentid' in form: sentid = form['sentid'].value
	else: sentid = ''
	if 'occ' in form: ocorrencias = form['occ'].value
	else: ocorrencias = ''
	text = form['textheader'].value
	conlluzao = estrutura_dados.LerUD('/interrogar-ud/conllu/' + ud)
	form['token'].value = form['token'].value.strip()
	if 'coluna' in form: form['coluna'].value = form['coluna'].value.strip()
	form['valor'].value = form['valor'].value.strip()
	data = str(datetime.now()).replace(' ','_').split('.')[0]

	try:
		if isinstance(conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1], list):
			antes = '\t'.join(conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1])
			conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1][int(form['coluna'].value)-1] = form['valor'].value
			depois = '\t'.join(conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1]).replace(form['valor'].value, '<b>' + form['valor'].value + '</b>')
		else:
			antes = conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1]
			conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1] = form['valor'].value
			depois = conlluzao[int(form['sentnum'].value)][int(form['token'].value)-1].replace(form['valor'].value, '<b>' + form['valor'].value + '</b>')

		estrutura_dados.EscreverUD(conlluzao, '/interrogar-ud/conllu/' + ud)

		if not os.path.isfile('/interrogar-ud/inqueritos.txt'):
			open('/interrogar-ud/inqueritos.txt', 'w').write('')

		inqueritos = open('/interrogar-ud/inqueritos.txt', 'r').read()
		inqueritos_cars = open('/interrogar-ud/inqueritos_cars.txt', 'r').read()
		inquerito_concluido = form['textheader'].value + '!@#' + antes + ' --> ' + depois + '!@#' + form['conllu'].value + '!@#' + data
		inquerito_concluido += '!@#' + form['nome_interrogatorio'].value + ' (' + form['occ'].value + ')' if 'occ' in form else '!@#NONE'
		inquerito_concluido += '!@#' + form['link_interrogatorio'].value if 'link_interrogatorio' in form else '!@#NONE'
		tag = form['tag'].value.replace('&lt;','<').replace('&gt;','>').replace(';', '_') if 'tag' in form else 'NONE'
		inquerito_concluido += '!@#' + tag if 'tag' in form else '!@#NONE'
		inquerito_concluido += '!@#' + form['sentid'].value if 'sentid' in form else '!@#NONE'
		open('/interrogar-ud/inqueritos.txt', 'w').write(inquerito_concluido + '\n' + inqueritos)
		if tag != 'NONE' and not tag in inqueritos_cars: open('/interrogar-ud/inqueritos_cars.txt', 'w').write(tag + '\n' + inqueritos_cars)

		html = '''<html><head>
				   <meta http-equiv="content-type" content="text/html; charset=UTF-8; width=device-width, initial-scale=1.0" name="viewport">
				 </head>
				 <body><form action="/cgi-bin/inquerito.py?conllu=''' + ud + '''" method="POST" id="reenviar"><input type=hidden name=sentid value="''' + sentid + '''"><input type=hidden name=occ value="''' + ocorrencias + '''"><input type="hidden" name="textheader" value="''' + text.replace('/BOLD','').replace('@BOLD','').replace('@YELLOW/', '').replace('@PURPLE/', '').replace('@BLUE/', '').replace('@RED/', '').replace('@CYAN/', '').replace('/FONT', '') + '''"><input type=hidden name="nome_interrogatorio" value="''' + nome + '''"><input type=hidden name="link_interrogatorio" value="''' + link + '''"><input type=hidden name=finalizado value=sim>'''
		if 'tag' in form: html += '<input type=hidden name=tag value="' + form['tag'].value + '">'
		html += '''</form>
				 <script>document.cookie = "tag=''' + tag + '''"; document.getElementById('reenviar').submit();</script></body></html>'''

	except Exception as e:
		print('Erro: ' + str(e))
		exit()

elif os.environ['REQUEST_METHOD'] != 'POST':
	printar()

elif os.environ['REQUEST_METHOD'] == 'POST' and form['action'].value == 'filtrar':
	coluna = form['coluna'].value
	valor = form['valor'].value
	printar(coluna, valor, form['onlysent'].value if 'onlysent' in form else False)

print(html)
