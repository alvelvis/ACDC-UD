#!/usr/bin/python3
# -*- coding: UTF-8 -*-

print("Content-type:text/html")
print('\n\n')

import os, sys
import cgi,cgitb
cgitb.enable()
import re

def printar(coluna = '', valor = ''):
	from estrutura_dados import slugify as slugify
	html = open('/interrogar-ud/index1.html', 'r').read()

	if not os.path.isfile('/interrogar-ud/queries.txt'): open('/interrogar-ud/queries.txt', 'w').write('')
	queries = open('/interrogar-ud/queries.txt', 'r').read().splitlines()
	queries = [x for x in queries if x.strip() != '']

	novo_html = ''

	criterios = open('/interrogar-ud/criterios.txt', 'r').read().split('!@#')

	novo_html += '<form action="/cgi-bin/interrogatorio.cgi" method="POST">Filtrar pesquisas:<br><select name="coluna" required><option value=":">Tudo</option><option value="1">Nome</option><option value="3">Critério de busca</option><option value="4">Expressão de busca</option><option value="5">CoNLLU</option><option value="6">Data</option></select> <input type=text name=valor value="' + valor + '" autofocus=true required> <input type=submit class="btn-gradient mini orange" value="Realizar filtro" style="display:block-inline">'

	if coluna: novo_html += ' <a style="display:block-inline" class="close-thik" href="/cgi-bin/interrogatorio.cgi"></a>'

	novo_html += '</form><br>'
	html_query = ''
	total = 0
	for query in queries:
		if query.strip():
			if (coluna != ':' and valor and len(query.split('\t')) >= int(coluna) + 1 and (re.search(valor, query.split('\t')[int(coluna)], flags=re.I|re.M))) or (not coluna) or (coluna == ':' and re.search(valor, query, flags=re.I|re.M)):
				html_query += '''<div class="container-lr" ><p><h3><a href="''' + query.split('\t')[0] + '''">''' + query.split('\t')[1] + ''' (''' + query.split('\t')[2] + ''')</a> <!--a class="close-thik" href="#" onclick='apagar("''' + query.split('\t')[0].split('resultados/')[1].split('.html')[0] + '''")'></a--></h3></p><p><div class="tooltip" style="display: inline-block">''' + query.split('\t')[3] + ''' ''' + query.split('\t')[4] + '''<span class="tooltiptext">''' + criterios[int(query.split('\t')[3])].split('<h4>')[0] + '''</span></div></p><small><p>''' + query.split('\t')[5] + '''</p><p>''' + query.split('\t')[6] + '''</p></small></div>\n''' # &nbsp;&nbsp;&nbsp;&nbsp;
				total += 1

	novo_html = html.split('<!--SPLIT-->')[0] + novo_html + 'Interrogações: ' + str(total) + '<br><br>' + html_query + html.split('<!--SPLIT-->')[1]

	print(novo_html)

if os.environ['REQUEST_METHOD'] != 'POST':
	printar()
else:
	form = cgi.FieldStorage()
	coluna = form['coluna'].value
	valor = form['valor'].value
	printar(coluna, valor)
