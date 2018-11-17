def atualizar():
	try:
		from git import Git
	except:
		from pip import main as pipmain
		pipmain(['install','GitPython'])
		print('GitPython instalado com sucesso!\nAtualize novamente...')
		exit()
	else:
		import os
		import shutil
		if os.path.isdir('.git'): shutil.rmtree('.git')
		Git().init()
		Git().remote('add','origin','https://github.com/alvelvis/ACDC-UD.git')
		Git().fetch()
		if os.path.isfile('atualizar_repo.py'): os.remove('atualizar_repo.py')
		if os.path.isfile('README.md'): os.remove('README.md')
		if os.path.isfile('acdc_procura.py'): os.remove('acdc_procura.py')
		if os.path.isfile('comparar_UD.py'): os.remove('comparar_UD.py')
		if os.path.isfile('limpar_conllu.py'): os.remove('limpar_conllu.py')
		if os.path.isfile('apenas_tokens.py'): os.remove('apenas_tokens.py')
		if os.path.isfile('tokenizar_conllu.py'): os.remove('tokenizar_conllu.py')
		if os.path.isfile('udpipe_vertical.py'): os.remove('udpipe_vertical.py')
		Git().checkout('master')

atualizar()
