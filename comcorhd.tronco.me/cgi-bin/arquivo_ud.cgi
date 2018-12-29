#!/usr/bin/python
# -*- coding: UTF-8 -*-

print("Content-type:text/html")
print('\n\n')

import os
import cgi,cgitb
cgitb.enable()
import re
import datetime
from estrutura_dados import slugify as slugify

#if not 'REQUEST_METHOD' in os.environ:
#	os.environ['REQUEST_METHOD'] = 'POST'

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

if os.environ['REQUEST_METHOD'] != 'POST':
    html = open('/interrogar-ud/arquivo_ud.html', 'r').read()
    html1 = html.split('<!--SPLIT-->')[0]
    html2 = html.split('<!--SPLIT-->')[1]

    if not os.path.isdir('/interrogar-ud/conllu'):
        os.mkdir('/interrogar-ud/conllu')

    uds = [x for x in os.listdir('/interrogar-ud/conllu') if os.path.isfile('/interrogar-ud/conllu/' + x)]

    for ud in uds:
	    html1 += '<div class="container-lr"><a href="/interrogar-ud/conllu/' + ud + '" download>' + ud + '</a> &nbsp;&nbsp; ' + str(len(open('/interrogar-ud/conllu/' + ud, 'r').read().split('\n\n'))) + ' sentenças &nbsp;&nbsp; ' + str(file_size('/interrogar-ud/conllu/' + ud)) + ' &nbsp;&nbsp; ' + str(datetime.datetime.fromtimestamp(os.path.getctime('/interrogar-ud/conllu/' + ud))).split('.')[0] + ''' &nbsp;&nbsp;&nbsp; <a href="#" onclick='apagar("''' + ud + '''")' ><em>excluir</em></a></div>\n'''

    novo_html = html1 + html2

    print(novo_html)


else:
    form = cgi.FieldStorage()
    f = os.path.basename(form['file'].filename)
    open('/interrogar-ud/conllu/' + slugify(f), 'wb').write(form['file'].file.read())
    print('<body onload="redirect()"><script>function redirect() { window.location = "/cgi-bin/arquivo_ud.cgi" }</script></body>')



