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
import functions
from functions import tabela

#if not 'REQUEST_METHOD' in os.environ:
#	os.environ['REQUEST_METHOD'] = 'POST'

from estrutura_dados import slugify as slugify

form = cgi.FieldStorage()

if not 'pesquisa' in form and not 'action' in form:
	html = '<head><title>Filtrar: Interrogatório</title></head>'
	html += '<body><form action="/cgi-bin/filtrar.cgi" method=POST>'
	html += '<select name="html">'
	for arquivo in os.listdir('/interrogar-ud/resultados'):
		if os.path.isfile('/interrogar-ud/resultados/' + arquivo):
			html += '<option value="' + arquivo.rsplit('.', 1)[0] + '">' + arquivo.rsplit('.', 1)[0] + '</option>'
	html += '</select><br><select name="udoriginal">'
	for arquivo in os.listdir('/interrogar-ud/conllu'):
		if os.path.isfile('/interrogar-ud/conllu/' + arquivo):
			html += '<option value="' + arquivo + '">' + arquivo + '</option>'
	html += '</select><br><br><input type="text" name="pesquisa" placeholder="Expressão do filtro"><br><input type="text" placeholder="Nome do filtro" name="nome_pesquisa"><br><br><input type="submit" value="Filtrar">'
	html += '</form></body>'
	print(html)

elif not 'action' in form or form['action'].value != 'desfazer':
	if ' ' in form['pesquisa'].value: parametros = form['pesquisa'].value.split(' ', 1)[1].replace('<b>', '').replace('<\\/b>','').replace('<font color="' + tabela['yellow'] + '">','').replace('<font color="' + tabela['red'] + '">','').replace('<font color="' + tabela['cyan'] + '">','').replace('<font color="' + tabela['blue'] + '">','').replace('<font color="' + tabela['purple'] + '">','').replace('<\\/font>','')
	if not re.match('^\d+$', form['pesquisa'].value.split(' ')[0]):
		criterio = '1'
		parametros = form['pesquisa'].value.replace('<b>','').replace('<\\/b>','').replace('<font color="' + tabela['yellow'] + '">','').replace('<font color="' + tabela['red'] + '">','').replace('<font color="' + tabela['cyan'] + '">','').replace('<font color="' + tabela['blue'] + '">','').replace('<font color="' + tabela['purple'] + '">','').replace('<\\/font>','')
		if not '^# text = ' in form['pesquisa'].value: print('<script>window.alert("Critério não especificado. Utilizando expressão regular (critério 1).")</script>')
	else:
		criterio = form['pesquisa'].value.split(' ')[0]

	if int(criterio) > int(open('/interrogar-ud/max_crit.txt', 'r').read().split()[0]):
		print('em desenvolvimento')
		exit()

	with open('/interrogar-ud/resultados/' + form['html'].value + '.html', 'r') as f:
		html = f.read()
		html = re.split(r'\<pre.*?\>', html)
		html = [x.split('</pre>')[0] for x in html[1:]]
		open('/interrogar-ud/conllu/tmp.conllu', 'w').write("\n\n".join(html).replace('<b>','').replace('</b>','').replace('<font color="' + tabela['yellow'] + '">','').replace('<font color="' + tabela['red'] + '">','').replace('<font color="' + tabela['cyan'] + '">','').replace('<font color="' + tabela['blue'] + '">','').replace('<font color="' + tabela['purple'] + '">','').replace('</font>',''))

	udoriginal = form['udoriginal'].value
	arquivo_ud = '/interrogar-ud/conllu/tmp.conllu'
	ud = "tmp.conllu"
	if not 'nome_pesquisa' in form:
		nome = form['pesquisa'].value.replace('<b>','').replace('</b>','').replace('<font color="' + tabela['yellow'] + '">','').replace('<font color="' + tabela['red'] + '">','').replace('<font color="' + tabela['cyan'] + '">','').replace('<font color="' + tabela['blue'] + '">','').replace('<font color="' + tabela['purple'] + '">','').replace('</font>','')
	else:
		nome = form['nome_pesquisa'].value
	if not os.path.isdir('/interrogar-ud/resultados/' + form['html'].value): os.mkdir('/interrogar-ud/resultados/' + form['html'].value)
	data = str(datetime.now()).replace(' ','_').split('.')[0]
	link = '/interrogar-ud/resultados/' + form['html'].value + '/' + slugify(nome) + '_' + data + '.html'

	lista_ocorrencias = interrogar_UD.main(arquivo_ud, int(criterio), parametros)

	print('Total: ' + str(len(lista_ocorrencias)))

	conllu_completo = open('/interrogar-ud/conllu/' + udoriginal, 'r').read().split('\n\n')

	ocorrencias = str(len(lista_ocorrencias))
	html = open('/interrogar-ud/resultados/link1.html', 'r').read().replace('../','../../')
	html1 = html.split('<!--SPLIT-->')[0]
	html2 = html.split('<!--SPLIT-->')[1]
	html_original = open('/interrogar-ud/resultados/' + form['html'].value + '.html', 'r').read().replace('<div class="content">','<div class="content"> > <a href="' + form['html'].value + '/' + slugify(nome) + '_' + data + '.html">' + nome + ' (' + ocorrencias  + ')</a>&nbsp;<a class="close-thik" alt="Desfazer filtro" href="/cgi-bin/filtrar.cgi?action=desfazer&html=' + link + '_anterior&original=' + form['html'].value + '"></a>&nbsp;')
	if not 'Com filtros: ' in html_original:
		ocorrencias_anterior = int(re.search(r'\((\d+)\)\</h1\>', html_original).group(1))
		html_original = re.sub(r'(\(.*?\)\</h1\>)', r'\1<br>Com filtros: ' + str(ocorrencias_anterior - int(ocorrencias)), html_original)
	else:
		ocorrencias_anterior = int(re.search(r'Com filtros: (\d+)', html_original).group(1))
		html_original = re.sub(r'Com filtros: \d+', 'Com filtros: ' + str(ocorrencias_anterior - int(ocorrencias)), html_original)

	for i, ocorrencia in enumerate(lista_ocorrencias):
		print(str(i+1) + '/' + str(len(lista_ocorrencias)))
		ocorrencia = ocorrencia.replace('<b>','@BOLD').replace('</b>','/BOLD').replace('<font color="' + tabela['yellow'] + '">','@YELLOW/').replace('<font color="' + tabela['red'] + '">','@RED/').replace('<font color="' + tabela['cyan'] + '">','@CYAN/').replace('<font color="' + tabela['blue'] + '">','@BLUE/').replace('<font color="' + tabela['purple'] + '">','@PURPLE/').replace('</font>','/FONT').replace('<','&lt;').replace('>','&gt;')

		if '# sent_id = ' in ocorrencia:
			sentid = ocorrencia.split('# sent_id = ')[1].split('\n')[0]
		else: sentid = ''
		if '# text = ' in ocorrencia:
			text = ocorrencia.split('# text = ')[1].split('\n')[0]
		else: text = ''

		novo =  '''<div class="container"><p>'''+str(i+1)+''' / '''+ocorrencias+'''</p>'''
		#SENTID
		if sentid != '': novo += '''<p>'''+sentid.replace('/BOLD','</b>').replace('@BOLD','<b>')+'''</p>'''
		#FORM
		novo += '''<form action="/cgi-bin/inquerito.py?conllu=''' + udoriginal + '''" target="_blank" method="POST" id="form_'''+str(i+1)+'''"><input type="hidden" name="textheader" value="''' + text.replace('/BOLD','').replace('@BOLD','').replace('@YELLOW/', '').replace('@PURPLE/', '').replace('@BLUE/', '').replace('@RED/', '').replace('@CYAN/', '').replace('/FONT', '') + '''"></form><form action="/cgi-bin/udpipe.py?conllu=''' + udoriginal + '''" target="_blank" method="POST" id="udpipe_'''+str(i+1)+'''"><input type="hidden" name="textheader" value="''' + text.replace('/BOLD','').replace('@BOLD','').replace('@YELLOW/', '').replace('@PURPLE/', '').replace('@BLUE/', '').replace('@RED/', '').replace('@CYAN/', '').replace('/FONT', '') + '''"></form>'''
		#TEXT
		novo += '''<p id="text_'''+str(i+1)+'''">'''+ text.replace('/BOLD','</b>').replace('@BOLD','<b>').replace('@YELLOW/', '<font color="' + tabela['yellow'] + '">').replace('@PURPLE/', '<font color="' + tabela['purple'] + '">').replace('@BLUE/', '<font color="' + tabela['blue'] + '">').replace('@RED/', '<font color="' + tabela['red'] + '">').replace('@CYAN/', '<font color="' + tabela['cyan'] + '">').replace('/FONT', '</font>')+ '''</p>
<p>'''

		#CONTEXTO
		if sentid != '' and text != '':
			if '-' in sentid or re.search('^\d+$', sentid):
				temcontexto = True
			else:
				temcontexto = False
		else:
			temcontexto = False

		if temcontexto:
			novo += '''<input id="contexto_'''+str(i+1)+'''" value="Mostrar contexto" onclick="contexto('divcontexto_'''+str(i+1)+'''', 'contexto_'''+str(i+1)+'''')" style="margin-left:0px" type="button"> <input id="mostrar_'''+str(i+1)+'''" class="anotacao" value="Mostrar anotação" onclick="mostrar('div_'''+str(i+1)+'''', 'mostrar_'''+str(i+1)+'''')" style="margin-left:0px" type="button"> <input id="opt_'''+str(i+1)+'''" class="opt" value="Mostrar opções" onclick="mostraropt('optdiv_'''+str(i+1)+'''', 'opt_'''+str(i+1)+'''')" style="margin-left:0px" type="button">'''
		else:
			novo += '''<input class="anotacao" id="mostrar_'''+str(i+1)+'''" value="Mostrar anotação" onclick="mostrar('div_'''+str(i+1)+'''', 'mostrar_'''+str(i+1)+'''')" style="margin-left:0px" type="button"> <input id="opt_'''+str(i+1)+'''" class="opt" value="Mostrar opções" onclick="mostraropt('optdiv_'''+str(i+1)+'''', 'opt_'''+str(i+1)+'''')" style="margin-left:0px" type="button">'''

		novo += '''</p>'''

		#Contexto e Anotação
		if temcontexto:
			if '-' in sentid:
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
				novo += '''<p id="divcontexto_'''+str(i+1)+'''" style="display:none">''' + contexto1 + ' ' + text.replace('/BOLD','</b>').replace('@BOLD','<b>').replace('@YELLOW/', '<font color="' + tabela['yellow'] + '">').replace('@PURPLE/', '<font color="' + tabela['purple'] + '">').replace('@BLUE/', '<font color="' + tabela['blue'] + '">').replace('@RED/', '<font color="' + tabela['red'] + '">').replace('@CYAN/', '<font color="' + tabela['cyan'] + '">').replace('/FONT', '</font>') + ' ' + contexto2 + '''</p>\n'''

			#IF NOT - in sentid
			else:
				try:
					sentnum = int(sentid)
					contexto1 = ''
					contexto2 = ''
					if sentnum == 1:
						contexto1 = '.'
					for sentence in conllu_completo:
						if '# sent_id = ' in sentence and '# text = ' in sentence:
							if contexto1 != '.':
								if int(sentence.split('# sent_id = ')[1].split('\n')[0]) == sentnum -1:
									contexto1 = sentence.split('# text = ')[1].split('\n')[0]
							if int(sentence.split('# sent_id = ')[1].split('\n')[0]) == sentnum +1:
								contexto2 = sentence.split('# text = ')[1].split('\n')[0]
							if (contexto1 != '' or contexto1 == '.') and contexto2 != '':
								break
					novo += '''<p id="divcontexto_'''+str(i+1)+'''" style="display:none">''' + contexto1 + ' ' + text.replace('/BOLD','</b>').replace('@BOLD','<b>').replace('@YELLOW/', '<font color="' + tabela['yellow'] + '">').replace('@PURPLE/', '<font color="' + tabela['purple'] + '">').replace('@BLUE/', '<font color="' + tabela['blue'] + '">').replace('@RED/', '<font color="' + tabela['red'] + '">').replace('@CYAN/', '<font color="' + tabela['cyan'] + '">').replace('/FONT', '</font>') + ' ' + contexto2 + '''</p>\n'''
				except:
					pass

		novo += '''<pre id="div_'''+str(i+1)+'''" style="display:none">''' + ocorrencia.replace('/BOLD','</b>').replace('@BOLD','<b>').replace('@YELLOW/', '<font color="' + tabela['yellow'] + '">').replace('@PURPLE/', '<font color="' + tabela['purple'] + '">').replace('@BLUE/', '<font color="' + tabela['blue'] + '">').replace('@RED/', '<font color="' + tabela['red'] + '">').replace('@CYAN/', '<font color="' + tabela['cyan'] + '">').replace('/FONT', '</font>') + '''</pre>'''

		#Fim contexto e anotação
		novo += '''<div style="display:none" id="optdiv_''' + str(i+1) + '''"><p><a style="cursor:pointer" onclick='inquerito("form_'''+str(i+1)+'''")'>[Abrir inquérito]</a> <a style="cursor:pointer" onclick='anotarudpipe("udpipe_'''+str(i+1)+'''")'>[Anotar no UDPipe]</a></p></div></div>\n'''

		html1 = html1 + novo

		html_original = html_original.split('<div class="container">')
		for i, sentence in enumerate(html_original):
			if i != 0:
				if '# text = ' + text.replace('<b>', '').replace('</b>', '').replace('/BOLD', '').replace('@BOLD', '').replace('<font color="' + tabela['yellow'] + '">', '').replace('<font color="' + tabela['red'] + '">', '').replace('<font color="' + tabela['cyan'] + '">', '').replace('<font color="' + tabela['blue'] + '">', '').replace('<font color="' + tabela['purple'] + '">', '').replace('</font>', '').replace('@YELLOW/', '').replace('@RED/', '').replace('@CYAN/','').replace('@BLUE/', '').replace('@PURPLE/', '').replace('/FONT', '') in sentence.replace('<b>', '').replace('</b>', '').replace('/BOLD', '').replace('@BOLD', '').replace('<font color="' + tabela['yellow'] + '">', '').replace('<font color="' + tabela['red'] + '">', '').replace('<font color="' + tabela['cyan'] + '">', '').replace('<font color="' + tabela['blue'] + '">', '').replace('<font color="' + tabela['purple'] + '">', '').replace('</font>', '').replace('@YELLOW/', '').replace('@RED/', '').replace('@CYAN/', '').replace('@BLUE/', '').replace('@PURPLE/', '').replace('/FONT', ''):
					if len(html_original[i].split('</div>')) > 1:
						html_original[i] = '</div>' + html_original[i].split('</div>', 1)[1]
					else:
						html_original[i] = '</div>'
		html_original = '<div class="container">'.join(html_original)

	os.remove('/interrogar-ud/conllu/tmp.conllu')

	html = html1 + html2

	html = html.replace('''<a style="cursor:pointer" onclick="tudo('marcar')">[Marcar tudo]</a> <a style="cursor:pointer" onclick="tudo('desmarcar')">[Desmarcar tudo]</a>''', "")

	#title
	novo_html = re.sub(re.escape('<title>link de pesquisa 1 (203): Interrogatório</title>'), '<title>' + nome + ' (' + ocorrencias + '): Interrogatório</title>', html)

	#h1
	novo_html = re.sub(re.escape('<h1><span id="combination">link de pesquisa 1</span> (203)</h1>'), '<h1><span id="combination">' + nome.replace('\\','\\\\') + '</span> (' + ocorrencias + ')</h1>', novo_html)

	#h2
	criterios = open('/interrogar-ud/criterios.txt', 'r').read().split('!@#')
	novo_html = re.sub(re.escape('<p>critério y#z#k&nbsp;&nbsp;&nbsp; arquivo_UD&nbsp;&nbsp;&nbsp; <span id="data">data</span>&nbsp;&nbsp;&nbsp;'), '<p><div class="tooltip">' + criterio + ' ' + parametros.replace('\\','\\\\') + '<span class="tooltiptext">' + criterios[int(criterio)].replace('\\','\\\\').split('<h4>')[0] + '</span></div> &nbsp;&nbsp;&nbsp;&nbsp; <div class="tooltip">Filtro<span class="tooltiptext">Página é resultado da filtragem de uma interrogação anterior.</span></div> &nbsp;&nbsp;&nbsp;&nbsp; <span id="data">' + data + '</span> &nbsp;&nbsp;&nbsp;&nbsp; ', novo_html)

	#apagar.cgi
	novo_html = re.sub('\<a.*onclick="apagar.*\</a\>', '', novo_html)
	novo_html = re.sub('\<button.*filtrar.*\n.*\</button\>', '', novo_html)
	novo_html = re.sub('/cgi-bin/conllu.cgi', '/cgi-bin/conllu.cgi?html=' + link, novo_html)

	open(link, 'w').write(novo_html.replace('<div class="content">','<div class="content"> > <a href="../' + form['html'].value + '.html">Voltar</a> > <a href="/cgi-bin/filtrar.cgi?action=desfazer&html=' + link + '_anterior&original='+form['html'].value+'">Desfazer este filtro</a>'))
	open(link + '_anterior', 'w').write(open('/interrogar-ud/resultados/' + form['html'].value + '.html', 'r').read())
	open('/interrogar-ud/resultados/' + form['html'].value + '.html', 'w').write(html_original)

	print('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8" /></head><body onload="redirect()"><script>function redirect() { window.location = "/interrogar-ud/resultados/' + form['html'].value + '.html" }</script></body>')

elif form['action'].value == 'desfazer':
	html = form['html'].value
	original = form['original'].value
	open('/interrogar-ud/resultados/' + original + '.html', 'w').write(open(html, 'r').read())

	print('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8" /></head><body onload="redirect()"><script>function redirect() { window.location = "/interrogar-ud/resultados/' + original + '.html" }</script></body>')
