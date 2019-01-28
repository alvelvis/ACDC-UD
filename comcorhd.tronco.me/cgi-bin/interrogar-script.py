#!/usr/bin/python3

print("Content-type: text/html\n\n")

import os
import cgi, cgitb
cgitb.enable()
from subprocess import call
import re

html = '<html><head><title>Executar script</title></head><body>'
print(html)

if os.environ['REQUEST_METHOD'] == 'POST':
	form = cgi.FieldStorage()
	inqueritos = open('/interrogar-ud/inqueritos.txt').read().splitlines()

	#pega os headers
	headers = list()
	for linha in open(form['link_interrogatorio'].value, 'r').read().splitlines():
		if '# text = ' in linha:
			headers.append(re.sub(r'\<.*?\>', '', linha))

	open('/interrogar-ud/scripts/headers.txt', 'w').write("\n".join(headers))
	call('python3 /interrogar-ud/scripts/' + form['script'].value + ' ' + form['conllu'].value, shell=True)
	for linha in open('/interrogar-ud/scripts/novos_inqueritos.txt', 'r').read().splitlines():
		inqueritos.insert(0, linha.rsplit('!@#', 1)[0] + '!@#' + form['nome_interrogatorio'].value + ' (' + form['occ'].value + ')!@#' + form['link_interrogatorio'].value + '!@#' + form['script'].value + '!@#' + linha.rsplit('!@#', 1)[1])

	open('/interrogar-ud/inqueritos.txt', 'w').write('\n'.join(inqueritos))
	os.remove('/interrogar-ud/scripts/novos_inqueritos.txt')
	os.remove('/interrogar-ud/scripts/headers.txt')
	
	html += '<form id="submeter" action="/cgi-bin/inquerito.py?action=filtrar" method="POST"><input type=hidden name=coluna value=6><input type=hidden name=valor value="' + form['script'].value + '"></form>'
	html += '<script>document.getElementById("submeter").submit()</script>'

html += '</body></html>'

print(html)