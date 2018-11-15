#Atualizar o repositório
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
		if os.path.isdir('.git'):
			Git().pull()
		else:
			Git().init()
			Git().remote('add','origin','https://github.com/alvelvis/ACDC-UD.git')
			Git().fetch()
			Git().checkout('master')
