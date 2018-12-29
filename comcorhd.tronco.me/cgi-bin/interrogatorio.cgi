#!/usr/bin/python3
# -*- coding: UTF-8 -*-

print("Content-type:text/html")
print('\n\n')

import os, sys
import cgi,cgitb
cgitb.enable()
import re

#if not 'REQUEST_METHOD' in os.environ:
#	os.environ['REQUEST_METHOD'] = 'POST'

from estrutura_dados import slugify as slugify
html = open('/interrogar-ud/index1.html', 'r').read()

if not os.path.isfile('/interrogar-ud/queries.txt'): open('/interrogar-ud/queries.txt', 'w').write('')
queries = open('/interrogar-ud/queries.txt', 'r').read().splitlines()
queries = [x for x in queries if x.strip() != '']

novo_html = ''

criterios = open('/interrogar-ud/criterios.txt', 'r').read().split('!@#')

for query in queries:
	novo_html = novo_html + '''<div class="container-lr" ><p><h3><a style="color:green" href="''' + query.split('\t')[0] + '''">''' + query.split('\t')[1] + ''' (''' + query.split('\t')[2] + ''')</a> <a class="close-thik" href="#" onclick='apagar("''' + query.split('\t')[0].split('resultados/')[1].split('.html')[0] + '''")'></a></h3></p><p><div class="tooltip" style="display: inline-block">''' + query.split('\t')[3] + ''' ''' + query.split('\t')[4] + '''<span class="tooltiptext">''' + criterios[int(query.split('\t')[3])].split('<h4>')[0] + '''</span></div></p><small><p>''' + query.split('\t')[5] + '''</p><p>''' + query.split('\t')[6] + '''</p></small></div>\n''' # &nbsp;&nbsp;&nbsp;&nbsp;

novo_html = html.split('<!--SPLIT-->')[0] + novo_html + html.split('<!--SPLIT-->')[1]

print(novo_html)
