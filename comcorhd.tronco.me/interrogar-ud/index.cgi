#!/usr/bin/python
# -*- coding: UTF-8 -*-

print("Content-type:text/html")
print('\n\n')

import os
import cgi,cgitb
cgitb.enable()
import re

#if not 'REQUEST_METHOD' in os.environ:
#	os.environ['REQUEST_METHOD'] = 'POST'

from estrutura_dados import slugify as slugify

html = open('index1.html', 'r').read()

if not os.path.isfile('queries.txt'): open('queries.txt', 'w').write('')
queries = open('queries.txt', 'r').read().splitlines()

novo_html = ''

criterios = open('criterios.txt', 'r').read().split('!@#')

for query in queries:
	novo_html = novo_html + '''<div class="container-lr"><a href="''' + query.split('\t')[0] + '''">''' + query.split('\t')[1] + ''' (''' + query.split('\t')[2] + ''')</a> &nbsp;&nbsp;&nbsp;&nbsp; <div class="tooltip">''' + query.split('\t')[3] + ''' ''' + query.split('\t')[4] + '''<span class="tooltiptext">''' + criterios[int(query.split('\t')[3])] + '''</span></div> &nbsp;&nbsp;&nbsp;&nbsp; ''' + query.split('\t')[5] + ''' &nbsp;&nbsp;&nbsp;&nbsp; ''' + query.split('\t')[6] + ''' &nbsp;&nbsp;&nbsp;&nbsp; <a href="#" onclick='apagar("''' + query.split('\t')[0].split('resultados/')[1].split('.html')[0] + '''")'><em>excluir</em></a></div>\n'''

novo_html = html.split('<!--SPLIT-->')[0] + novo_html + html.split('<!--SPLIT-->')[1]

print(novo_html)
