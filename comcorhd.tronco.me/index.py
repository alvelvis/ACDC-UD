#!/usr/bin/python3
print('Content-type:text/html')
print('\n\n')

print('<head><title>ComCorHd</title></head><body>')

import os
for pasta in os.listdir('.'):
	if os.path.isdir(pasta) and pasta != 'cgi-bin':
		print('<h1><a href="' + pasta + '">' + pasta + '</a></h1><hr>')

print('</body>')
