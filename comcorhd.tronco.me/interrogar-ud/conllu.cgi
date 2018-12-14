#!/usr/bin/python
# -*- coding: UTF-8 -*-

print("Content-type:text/html")
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
with open(form['html'].value, 'r') as f:
	html = f.read()
	html = re.split(r'\<pre.*?\>', html)
	html = [x.split('</pre>')[0] for x in html[1:]]
	open('tmp/' + slugify(form['nomeconllu'].value) + '.conllu', 'w').write("\n".join(html).replace('<b>','').replace('</b>','') + '\n')

print('<head><meta http-equiv="content-type" content="text/html; charset=UTF-8" /></head><body onload="redirect()"><a href="tmp/'+slugify(form['nomeconllu'].value)+'.conllu" download target="_blank" id="download" hidden></a><script>function redirect() { document.getElementById("download").click(); window.location="' + form['html'].value + '" }</script></body>')

