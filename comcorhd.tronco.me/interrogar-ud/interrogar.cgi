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

	print(html.split('<select name="conllu">')[0] + '<select name="conllu">' + "\n".join(arquivos) + '</select>' + html.split('</select>')[1])


#POST
else:
	form = cgi.FieldStorage()
	if ' ' in form['pesquisa'].value: parametros = form['pesquisa'].value.split(' ', 1)[1]
	if not re.match('^\d+$', form['pesquisa'].value.split(' ')[0]):
		criterio = '1'
		parametros = form['pesquisa'].value
	else:
		criterio = form['pesquisa'].value.split(' ')[0]

	if int(criterio) > int(open('max_crit.txt', 'r').read().split()[0]):
		print('em desenvolvimento')
		exit()

	arquivo_ud = 'conllu/' + os.listdir('conllu')[int(form["conllu"].value)]
	ud = os.listdir('conllu')[int(form["conllu"].value)]
	nome = form['nome'].value
	data = str(datetime.now()).replace(' ','_').split('.')[0]
	link = 'resultados/' + slugify(nome) + '_' + data + '.html'

	lista_ocorrencias = list()
	for ocorrencia in interrogar_UD.main(arquivo_ud, int(criterio), parametros):
		lista_ocorrencias.append(ocorrencia)

	ocorrencias = str(len(lista_ocorrencias))
	html = open('resultados/link1.html', 'r').read()
	html = html.replace('filtrar.cgi', 'filtrar.cgi?html=' + slugify(nome) + '_' + data)
	html = html.replace('conllu.cgi', 'conllu.cgi?html=resultados/' + slugify(nome) + '_' + data + '.html')
	html1 = html.split('<!--SPLIT-->')[0]
	html2 = html.split('<!--SPLIT-->')[1]

	for i, ocorrencia in enumerate(lista_ocorrencias):
		ocorrencia = ocorrencia.replace('<b>','BOLD').replace('</b>','/BOLD').replace('<','&lt;').replace('>','&gt;')
		sentid = ''
		text = ''
		for linha in ocorrencia.splitlines():
			if '# sent_id = ' in linha.replace('<b>','').replace('</b>',''):
				sentid = linha
			if '# text = ' in linha.replace('<b>','').replace('</b>',''):
				text = linha
			if sentid != '' and text != '':
				break
		html1 = html1 + '''<div class="container">
<p>'''+str(i+1)+''' / '''+ocorrencias+'''</p>
<p><input id="checkbox_'''+str(i+1)+'''" style="margin-left:0px;" type="checkbox"> '''+sentid.replace('/BOLD','</b>').replace('BOLD','<b>')+'''</p>
<p id="text_'''+str(i+1)+'''">'''+text.replace('/BOLD','</b>').replace('BOLD','<b>')+'''</p>
<p><input id="mostrar_'''+str(i+1)+'''" value="Mostrar anotação" onclick="mostrar('div_'''+str(i+1)+'''', 'mostrar_'''+str(i+1)+'''')" style="margin-left:0px" type="button"></p>
<pre id="div_'''+str(i+1)+'''" style="display:none">'''+ocorrencia.replace('/BOLD','</b>').replace('BOLD','<b>')+'''
</pre><p><a href="#">Voltar ao topo</a></p></div>\n'''

	html = html1 + html2

	html1 = html.split('//TUDO')[0]
	html2 = html.split('//TUDO')[1]
	for i, ocorrencia in enumerate(lista_ocorrencias):
		html1 += 'if (document.getElementById("checkbox_'+str(i+1)+'")) {\n if (event == "marcar") {\n document.getElementById("checkbox_'+str(i+1)+'").checked = true \n} if (event == "desmarcar") {\n document.getElementById("checkbox_'+str(i+1)+'").checked = false \n} \n}\n'
		html1 += 'if (document.getElementById("mostrar_'+str(i+1)+'")) {\n if (event == "abrir") {\n if (document.getElementById("mostrar_'+str(i+1)+'").value == "Mostrar anotação") {\n document.getElementById("mostrar_'+str(i+1)+'").click() \n} \n} if (event == "fechar") {\n if (document.getElementById("mostrar_'+str(i+1)+'").value == "Esconder anotação") {\n document.getElementById("mostrar_'+str(i+1)+'").click() \n} \n} \n}'

	html = html1 + html2

	html1 = html.split('//SELECTION')[0]
	html2 = html.split('//SELECTION')[1]
	for i, ocorrencia in enumerate(lista_ocorrencias):
		html1 += 'if (document.getElementById("checkbox_'+str(i+1)+'")) {\n if (document.getElementById("checkbox_'+str(i+1)+'").checked == true) {\n document.getElementById("pesquisa").value = document.getElementById("pesquisa").value + "^" + escapeRegExp(document.getElementById("text_'+str(i+1)+'").innerHTML) + "$|"; \n} \n}\n'

	html = html1 + html2


	#title
	novo_html = re.sub(re.escape('<title>link de pesquisa 1 (203): Interrogatório</title>'), '<title>' + nome + ' (' + ocorrencias + '): Interrogatório</title>', html)

	#h1
	novo_html = re.sub(re.escape('<h1><span id="combination">link de pesquisa 1</span> (203)</h1>'), '<h1><span id="combination">' + nome + '</span> (' + ocorrencias + ')</h1>', novo_html)

	#h2
	criterios = open('criterios.txt', 'r').read().split('!@#')
	novo_html = re.sub(re.escape('<p>critério y#z#k&nbsp;&nbsp;&nbsp; arquivo_UD&nbsp;&nbsp;&nbsp; <span id="data">data</span>&nbsp;&nbsp;&nbsp;'), '<p><div class="tooltip">' + criterio + ' ' + parametros.replace('\\','\\\\') + '<span class="tooltiptext">' + criterios[int(criterio)].replace('\\','\\\\') + '</span></div> &nbsp;&nbsp;&nbsp;&nbsp; ' + ud + ' &nbsp;&nbsp;&nbsp;&nbsp; <span id="data">' + data + '</span> &nbsp;&nbsp;&nbsp;&nbsp; ', novo_html)

	#apagar.cgi
	novo_html = re.sub(re.escape('window.location = "../apagar.cgi?query=link1"'), 'window.location = "../apagar.cgi?query=' + slugify(nome) + '_' + data + '"', novo_html)

	open(link, 'w').write(novo_html)

	queries = [link + '\t' + nome + '\t' + ocorrencias + '\t' + criterio + '\t' + parametros + '\t' + ud + '\t' + data]
	queries.extend(open('queries.txt', 'r').read().splitlines())

	open('queries.txt', 'w').write("\n".join(queries))

	print('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8" /></head><body onload="redirect()"><script>function redirect() { window.location = "'+link+'" }</script></body>')


