#!/usr/bin/python3
# -*- coding: UTF-8 -*-

print("Content-type:text/html")
print('\n\n')

import os
import cgi, cgitb
cgitb.enable()

html = str()
html += '<head><meta name="viewport" content="width=device-width, initial-scale=1.0" charset="utf-8"></head><body>'

for arquivo in os.listdir('.'):
	if '.html' in arquivo:
		html += '<a href="' + arquivo + '"><h1>' + arquivo.split('.html')[0] + '</h1></a><hr>'

html += '</body>'

print(html)
