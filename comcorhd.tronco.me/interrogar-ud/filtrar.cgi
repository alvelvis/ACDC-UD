#!/usr/bin/python3
# -*- coding: UTF-8 -*-

print("Content-type:text/html; charset=utf-8")
print('\n\n')

import os
import cgi,cgitb
cgitb.enable()
import re
import estrutura_dados
import interrogar_UD
from datetime import datetime

#if not 'REQUEST_METHOD' in os.environ:
#	os.environ['REQUEST_METHOD'] = 'POST'

from estrutura_dados import slugify as slugify

#POST
form = cgi.FieldStorage()
if not 'action' in form or form['action'].value != 'desfazer':
	if ' ' in form['pesquisa'].value: parametros = form['pesquisa'].value.split(' ', 1)[1].replace('<b>','').replace('<\\/b>','')
	if not re.match('^\d+$', form['pesquisa'].value.split(' ')[0]):
		criterio = '1'
		parametros = form['pesquisa'].value.replace('<b>','').replace('<\\/b>','')
	else:
		criterio = form['pesquisa'].value.split(' ')[0]

	if int(criterio) > int(open('max_crit.txt', 'r').read().split()[0]):
		print('em desenvolvimento')
		exit()

	with open('resultados/' + form['html'].value + '.html', 'r') as f:
		html = f.read()
		html = re.split(r'\<pre.*?\>', html)
		html = [x.split('</pre>')[0] for x in html[1:]]
		open('conllu/tmp.conllu', 'w').write("\n".join(html).replace('<b>','').replace('</b>',''))

	arquivo_ud = 'conllu/tmp.conllu'
	ud = "tmp.conllu"
	if not 'nome_pesquisa' in form:
		nome = form['pesquisa'].value
	else:
		nome = form['nome_pesquisa'].value
	if not os.path.isdir('resultados/' + form['html'].value): os.mkdir('resultados/' + form['html'].value)
	data = str(datetime.now()).replace(' ','_').split('.')[0]
	link = 'resultados/' + form['html'].value + '/' + slugify(nome) + '_' + data + '.html'

	lista_ocorrencias = list()
	for ocorrencia in interrogar_UD.main(arquivo_ud, int(criterio), parametros):
		lista_ocorrencias.append(ocorrencia)

	ocorrencias = str(len(lista_ocorrencias))
	html = open('resultados/link1.html', 'r').read().replace('../','../../')
	html1 = html.split('<!--SPLIT-->')[0]
	html2 = html.split('<!--SPLIT-->')[1]
	html_original = open('resultados/' + form['html'].value + '.html', 'r').read().replace('<div class="content">','<div class="content"> > <a href="' + form['html'].value + '/' + slugify(nome) + '_' + data + '.html">' + nome + ' (' + ocorrencias  + ')</a>&nbsp;<a class="close-thik" alt="Desfazer filtro" href="../filtrar.cgi?action=desfazer&html=' + link + '_anterior&original=' + form['html'].value + '"></a>&nbsp;')
	if not 'Com filtros: ' in html_original:
		ocorrencias_anterior = int(re.search(r'\((.*)\)\</h1\>', html_original).group(1))
		html_original = re.sub(r'\((.*)\)\</h1\>', '(\1)</h1><br>Com filtros: ' + str(ocorrencias_anterior - int(ocorrencias)), html_original)
	else:
		ocorrencias_anterior = int(re.search(r'Com filtros: (\d+)', html_original).group(1))
		html_original = re.sub(r'Com filtros: \d+', 'Com filtros: ' + str(ocorrencias_anterior - int(ocorrencias)), html_original)

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
		novo =  '''<div class="container">
	<p>'''+str(i+1)+''' / '''+ocorrencias+'''</p>
	<p>'''+sentid.replace('/BOLD','</b>').replace('BOLD','<b>')+''' <input id="checkbox_'''+str(i+1)+'''" style="margin-left:0px;" type="checkbox"></p>
	<p>'''+text.replace('/BOLD','</b>').replace('BOLD','<b>')+'''</p>
	<p>Comentários: &nbsp;<input id="comment_'''+str(i+1)+'''" size="40px" type="text"></p><p><input id="mostrar_'''+str(i+1)+'''" value="Mostrar anotação" onclick="mostrar('div_'''+str(i+1)+'''', 'mostrar_'''+str(i+1)+'''')" style="margin-left:0px" type="button"></p>
	<pre id="div_'''+str(i+1)+'''" style="display:none">'''+ocorrencia.replace('/BOLD','</b>').replace('BOLD','<b>')+'''
	</pre><p><a href="#">Voltar ao topo</a></p></div>\n'''
		html1 = html1 + novo

		html_original = html_original.split('<div class="container">')
		for i, sentence in enumerate(html_original):
			if text.replace('<b>','').replace('</b>','') in sentence.replace('<b>','').replace('</b>',''):
				if len(html_original[i].split('</div>')) > 1:
					html_original[i] = '</div>' + html_original[i].split('</div>', 1)[1]
				else:
					html_original[i] = '</div>'
		html_original = '<div class="container">'.join(html_original)

	os.remove('conllu/tmp.conllu')

	html = html1 + html2
	html1 = html.split('//COMMENT')[0]
	html2 = html2.split('//COMMENT')[1]
	for i, ocorrencia in enumerate(lista_ocorrencias):
		html1 = html1 + '\ndocument.getElementById("comment_'+str(i+1)+'").value = url.searchParams.get("comment_'+str(i+1)+'")'
		html1 = html1 + '\nif (url.searchParams.get("checkbox_'+str(i+1)+'") == "true") { document.getElementById("checkbox_'+str(i+1)+'").checked = url.searchParams.get("checkbox_'+str(i+1)+'") }'

	html = html1 + html2

	html1 = html.split('//ENVIAR')[0]
	html2 = html.split('//ENVIAR')[1]
	link_query = ''
	for i, ocorrencia in enumerate(lista_ocorrencias):
		link_query += ' + "comment_'+str(i+1)+'=" + document.getElementById("comment_'+str(i+1)+'").value.replace(/\?/g, "~").replace(/\&/g, "~").replace(/\//g,"~") + "&"'
		link_query += ' + "checkbox_'+str(i+1)+'=" + document.getElementById("checkbox_'+str(i+1)+'").checked + "&"'
	html1 = html1 + 'document.getElementById("link_edit"+id).value = window.location.href.split("?")[0] + "?"' + link_query

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
	novo_html = re.sub(re.escape('<title>link de pesquisa 1 (203): Interrogar UD</title>'), '<title>' + nome + ' (' + ocorrencias + '): Interrogar UD</title>', html)

	#h1
	novo_html = re.sub(re.escape('<h1><span id="combination">link de pesquisa 1</span> (203)</h1>'), '<h1><span id="combination">' + nome.replace('\\','\\\\') + '</span> (' + ocorrencias + ')</h1>', novo_html)

	#h2
	criterios = open('criterios.txt', 'r').read().split('!@#')
	novo_html = re.sub(re.escape('<p>critério y#z#k&nbsp;&nbsp;&nbsp; arquivo_UD&nbsp;&nbsp;&nbsp; <span id="data">data</span>&nbsp;&nbsp;&nbsp;'), '<p><div class="tooltip">' + criterio + ' ' + parametros.replace('\\','\\\\') + '<span class="tooltiptext">' + criterios[int(criterio)].replace('\\','\\\\') + '</span></div> &nbsp;&nbsp;&nbsp;&nbsp; <div class="tooltip">Filtro<span class="tooltiptext">Página é resultado da filtragem de uma interrogação anterior.</span></div> &nbsp;&nbsp;&nbsp;&nbsp; <span id="data">' + data + '</span> &nbsp;&nbsp;&nbsp;&nbsp; ', novo_html)

	#apagar.cgi
	novo_html = re.sub('\<a.*onclick="apagar.*\</a\>', '', novo_html)
	novo_html = re.sub('\<button.*filtrar.*\n.*\</button\>', '', novo_html)
	novo_html = re.sub('conllu.cgi', 'conllu.cgi?html=' + link, novo_html)

	open(link, 'w').write(novo_html.replace('<div class="content">','<div class="content"> > <a href="../' + form['html'].value + '.html">Voltar</a> > <a href="../../filtrar.cgi?action=desfazer&html=' + link + '_anterior&original='+form['html'].value+'">Desfazer este filtro</a>'))
	open(link + '_anterior', 'w').write(open('resultados/' + form['html'].value + '.html', 'r').read())
	open('resultados/' + form['html'].value + '.html', 'w').write(html_original)

	print('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8" /></head><body onload="redirect()"><script>function redirect() { window.location = "resultados/' + form['html'].value + '.html" }</script></body>')

elif form['action'].value == 'desfazer':
	html = form['html'].value
	original = form['original'].value
	open('resultados/' + original + '.html', 'w').write(open(html, 'r').read())

	print('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8" /></head><body onload="redirect()"><script>function redirect() { window.location = "resultados/' + original + '.html" }</script></body>')
