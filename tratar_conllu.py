# -*- coding: utf-8 -*-

import os
import sys

if len(sys.argv) < 2:
	conllu = input('Arraste o arquivo .conllu: ').replace('\\','/').replace('"','').replace("'","").strip()
else:
	conllu = sys.argv[1]
arquivo = open(conllu, 'r').read().splitlines()
novo_conllu = list()
for linha in arquivo:
	if not '# d2d' in linha:
		novo_conllu.append(linha)
for a, linha in enumerate(novo_conllu):
	if len(linha.split('\t')) > 2:
		novo_conllu[a] = linha.split('\t')
		novo_conllu[a][4] = '_'
		#novo_conllu[a][9] = '_'
		novo_conllu[a] = "\t".join(novo_conllu[a])

open(conllu.rsplit('.conllu')[0] + '_editado.conllu', 'w').write('\n'.join(novo_conllu))
