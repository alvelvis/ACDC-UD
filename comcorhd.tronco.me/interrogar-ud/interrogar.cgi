#!/usr/bin/python3
# -*- coding: UTF-8 -*-

print("Content-type:text/html; charset=utf-8")
print('\n\n')

import os
import cgi,cgitb
cgitb.enable()
import re
import estrutura_dados
from estrutura_dados import slugify as slugify
import interrogar_UD
from datetime import datetime
import functions
from functions import tabela

#if not 'REQUEST_METHOD' in os.environ:
#	os.environ['REQUEST_METHOD'] = 'POST'

#GET
if os.environ['REQUEST_METHOD'] != "POST":

	arquivos = list()
	for i, arquivo in enumerate(os.listdir('conllu')):
		arquivos.append('<option value ="'+str(i)+'">'+arquivo+'</option>')
	html = open('interrogar_UDnew.html', 'r').read()
	html1 = html.split('<!--SPLIT-->')[0]
	html2 = html.split('<!--SPLIT-->')[1]

	criterios = open('criterios.txt', 'r').read().split('!@#')
	for criterio in criterios[1:]:
		html1 += '<div class="container-lr">' + criterio + '</div>\n'
	html = html1 + html2

	html1 = html.split('<!--SPLIT2-->')[0]
	html2 = html.split('<!--SPLIT2-->')[1]

	criterios = open('criterios.txt', 'r').read().split('!@#')
	for criterio in criterios[1:]:
		html1 += "\n".join(criterio.splitlines()[0:3]) + '\n'
	html = html1 + html2

	print(html.split('<select name="conllu">')[0] + '<select name="conllu">' + "\n".join(arquivos) + '</select>' + html.split('</select>')[1])


#POST
else:
	#Variáveis de POST
	form = cgi.FieldStorage()

	#Criterio e Pesquisa
	if ' ' in form['pesquisa'].value: parametros = form['pesquisa'].value.split(' ', 1)[1]
	if not re.match('^\d+$', form['pesquisa'].value.split(' ')[0]):
		criterio = '1'
		parametros = form['pesquisa'].value
		print('<script>window.alert("Critério não especificado. Utilizando expressão regular (critério 1)")</script>')
	else:
		criterio = form['pesquisa'].value.split(' ')[0]

	#Checa quantidade de critérios
	if int(criterio) > int(open('max_crit.txt', 'r').read().split()[0]):
		print('em desenvolvimento')
		exit()

	#Arquivo UD, Nome, Data, Link
	arquivo_ud = 'conllu/' + os.listdir('conllu')[int(form["conllu"].value)]
	ud = os.listdir('conllu')[int(form["conllu"].value)]
	nome = form['nome'].value
	data = str(datetime.now()).replace(' ','_').split('.')[0]
	link = 'resultados/' + slugify(nome) + '_' + data + '.html'

	#Ocorrências da pesquisa Interrogar_UD.py
	lista_ocorrencias = list()
	for ocorrencia in interrogar_UD.main(arquivo_ud, int(criterio), parametros):
		lista_ocorrencias.append(ocorrencia)
	ocorrencias = str(len(lista_ocorrencias))

	#Abre o arquivo conllu
	conllu_completo = open(arquivo_ud, 'r').read().split('\n\n')

	#Abre o arquivo LINK1 e dá replace no FILTRAR e CONLLU
	html = open('resultados/link1.html', 'r').read()
	html = html.replace('filtrar.cgi', 'filtrar.cgi?html=' + slugify(nome) + '_' + data + '&originalud=' + ud)
	html = html.replace('conllu.cgi', 'conllu.cgi?html=resultados/' + slugify(nome) + '_' + data + '.html')
	html1 = html.split('<!--SPLIT-->')[0]
	html2 = html.split('<!--SPLIT-->')[1]

	#PARA CADA OCORRÊNCIA DA PESQUISA
	for i, ocorrencia in enumerate(lista_ocorrencias):
		ocorrencia = ocorrencia.replace('<b>','@BOLD').replace('</b>','/BOLD').replace('<font color="' + tabela['yellow'] + '">','@YELLOW/').replace('<font color="' + tabela['red'] + '">','@RED/').replace('<font color="' + tabela['cyan'] + '">','@CYAN/').replace('<font color="' + tabela['blue'] + '">','@BLUE/').replace('<font color="' + tabela['purple'] + '">','@PURPLE/').replace('</font>','/FONT').replace('<','&lt;').replace('>','&gt;')

		#PROCURA SENTID E TEXT
		if '# sent_id = ' in ocorrencia:
			sentid = ocorrencia.split('# sent_id = ')[1].split('\n')[0]
		else: sentid = ''
		if '# text = ' in ocorrencia:
			text = ocorrencia.split('# text = ')[1].split('\n')[0]
		else: text = ''

		#ADICIONA O CONTAINER
		html1 = html1 + '''<div class="container">
<p>'''+str(i+1)+''' / '''+ocorrencias+'''</p>'''
		if sentid != '': html1 += '''<p><input id="checkbox_'''+str(i+1)+'''" style="margin-left:0px;" type="checkbox"> '''+sentid.replace('/BOLD','</b>').replace('@BOLD','<b>')+'''</p>'''
		html1 += '''<p id="text_'''+str(i+1)+'''">''' + text.replace('/BOLD','</b>').replace('@BOLD','<b>').replace('@YELLOW/', '<font color="' + tabela['yellow'] + '">').replace('@PURPLE/', '<font color="' + tabela['purple'] + '">').replace('@BLUE/', '<font color="' + tabela['blue'] + '">').replace('@RED/', '<font color="' + tabela['red'] + '">').replace('@CYAN/', '<font color="' + tabela['cyan'] + '">').replace('/FONT', '</font>') + '''</p>
<p>'''

		#CONTEXTO
		if sentid != '' and text != '':
			html1 += '''<input id="contexto_'''+str(i+1)+'''" value="Mostrar contexto" onclick="contexto('divcontexto_'''+str(i+1)+'''', 'contexto_'''+str(i+1)+'''')" style="margin-left:0px" type="button"> <input id="mostrar_'''+str(i+1)+'''" value="Mostrar anotação" onclick="mostrar('div_'''+str(i+1)+'''', 'mostrar_'''+str(i+1)+'''')" style="margin-left:0px" type="button">'''
		else:
			html1 += '''<input id="mostrar_'''+str(i+1)+'''" value="Mostrar anotação" onclick="mostrar('div_'''+str(i+1)+'''', 'mostrar_'''+str(i+1)+'''')" style="margin-left:0px" type="button">'''

		html1 += '''</p>'''

		#CONTEXTO E ANOTAÇÃO
		if sentid != '' and text != '':
			sentnum = int(sentid.split('-')[1].split()[0])
			sentnome = sentid.split('-')[0]
			contexto1 = ''
			contexto2 = ''
			if sentnum == 1:
				contexto1 = '.'
			for sentence in conllu_completo:
				if '# sent_id = ' in sentence and '# text = ' in sentence:
					if contexto1 != '.':
						if sentence.split('# sent_id = ')[1].split('-')[0] == sentnome and int(sentence.split('# sent_id = ')[1].split('-')[1].split('\n')[0]) == sentnum -1:
							contexto1 = sentence.split('# text = ')[1].split('\n')[0]
					if sentence.split('# sent_id = ')[1].split('-')[0] == sentnome and int(sentence.split('# sent_id = ')[1].split('-')[1].split('\n')[0]) == sentnum +1:
						contexto2 = sentence.split('# text = ')[1].split('\n')[0]
					if (contexto1 != '' or contexto1 == '.') and contexto2 != '':
						break
			html1 += '''<p id="divcontexto_'''+str(i+1)+'''" style="display:none">''' + contexto1 + ' ' + text.replace('/BOLD','</b>').replace('@BOLD','<b>').replace('@YELLOW/', '<font color="' + tabela['yellow'] + '">').replace('@PURPLE/', '<font color="' + tabela['purple'] + '">').replace('@BLUE/', '<font color="' + tabela['blue'] + '">').replace('@RED/', '<font color="' + tabela['red'] + '">').replace('@CYAN/', '<font color="' + tabela['cyan'] + '">').replace('/FONT', '</font>') + ' ' + contexto2 + '''</p>\n'''

		html1 += '''<pre id="div_'''+str(i+1)+'''" style="display:none">''' + ocorrencia.replace('/BOLD','</b>').replace('@BOLD','<b>').replace('@YELLOW/', '<font color="' + tabela['yellow'] + '">').replace('@PURPLE/', '<font color="' + tabela['purple'] + '">').replace('@BLUE/', '<font color="' + tabela['blue'] + '">').replace('@RED/', '<font color="' + tabela['red'] + '">').replace('@CYAN/', '<font color="' + tabela['cyan'] + '">').replace('/FONT', '</font>') + '''</pre>'''

		#Fim contexto e anotação
		html1 += '''<p><a href="#">Voltar ao topo</a></p></div>\n'''

	html = html1 + html2

	#ABRIR/FECHAR ANOTAÇÕES
	html = functions.tudo(html, lista_ocorrencias)

	#MARCAR/DESMARCAR TUDO
	html1 = html.split('//SELECTION')[0]
	html2 = html.split('//SELECTION')[1]
	for i, ocorrencia in enumerate(lista_ocorrencias):
		html1 += 'if (document.getElementById("checkbox_'+str(i+1)+'")) {\n if (document.getElementById("checkbox_'+str(i+1)+'").checked == true) {\n document.getElementById("pesquisa").value = document.getElementById("pesquisa").value + "^# text = (" + escapeRegExp(document.getElementById("text_'+str(i+1)+'").innerHTML) + ")$|"; \n} \n}\n'

	html = html1 + html2

	#title
	novo_html = re.sub(re.escape('<title>link de pesquisa 1 (203): Interrogatório</title>'), '<title>' + nome + ' (' + ocorrencias + '): Interrogatório</title>', html)

	#h1 - NOME DA QUERY
	novo_html = re.sub(re.escape('<h1><span id="combination">link de pesquisa 1</span> (203)</h1>'), '<h1><span id="combination">' + nome + '</span> (' + ocorrencias + ')</h1>', novo_html)

	#h2 - METADADOS DA QUERY
	criterios = open('criterios.txt', 'r').read().split('!@#')
	novo_html = re.sub(re.escape('<p>critério y#z#k&nbsp;&nbsp;&nbsp; arquivo_UD&nbsp;&nbsp;&nbsp; <span id="data">data</span>&nbsp;&nbsp;&nbsp;'), '<p><div class="tooltip">' + criterio + ' ' + parametros.replace('\\','\\\\') + '<span class="tooltiptext">' + criterios[int(criterio)].replace('\\','\\\\') + '</span></div> &nbsp;&nbsp;&nbsp;&nbsp; ' + ud + ' &nbsp;&nbsp;&nbsp;&nbsp; <span id="data">' + data + '</span> &nbsp;&nbsp;&nbsp;&nbsp; ', novo_html)

	#APAGAR.CGI
	novo_html = re.sub(re.escape('window.location = "../apagar.cgi?query=link1"'), 'window.location = "../apagar.cgi?query=' + slugify(nome) + '_' + data + '"', novo_html)

	open(link, 'w').write(novo_html)

	queries = [link + '\t' + nome + '\t' + ocorrencias + '\t' + criterio + '\t' + parametros + '\t' + ud + '\t' + data]
	queries.extend(open('queries.txt', 'r').read().splitlines())

	open('queries.txt', 'w').write("\n".join(queries))

	print('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8" /></head><body onload="redirect()"><script>function redirect() { window.location = "'+link+'" }</script></body>')


