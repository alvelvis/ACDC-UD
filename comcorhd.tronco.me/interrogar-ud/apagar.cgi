#!/usr/bin/python3
# -*- coding: UTF-8 -*-

print("Content-type:text/html")
print('\n\n')

import os
import cgi,cgitb
cgitb.enable()
from estrutura_dados import slugify as slugify

form = cgi.FieldStorage()
link = 'resultados/' + form["query"].value + '.html'

print('''<head>
           <meta http-equiv="content-type" content="text/html; charset=UTF-8">
         </head>''')

if os.path.isfile(link):
	import shutil
	os.rename(link, 'tmp/' + form['query'].value + '.html')
	if os.path.isdir('resultados/' + form["query"].value):
		shutil.move('resultados/' + form["query"].value, 'tmp/')
	queries = open('queries.txt', 'r', encoding="utf-8").read().splitlines()
	for i, query in enumerate(queries):
		if slugify(query.split('\t')[1]) + '_' + query.split('\t')[6] == form["query"].value:
			queries.pop(i)
			break

	open('queries.txt','w').write("\n".join(queries))

	print('<body onload="redirect()"><script>function redirect() { window.location = "index.cgi" }</script></body>')

else:
	queries = open('queries.txt', 'r', encoding="utf-8").read().splitlines()
	for i, query in enumerate(queries):
		if slugify(query.split('\t')[1]) + '_' + query.split('\t')[6] == form["query"].value:
			queries.pop(i)
			break

	open('queries.txt','w').write("\n".join(queries))

	print('<body onload="redirect()"><script>function redirect() { window.location = "index.cgi" }</script></body>')




