lista_arquivos = [
    'atualizar_repo.py',
    'README.md',
    'acdc_procura.py',
    'comparar_UD.py',
    'revisar_UD.py',
    'limpar_conllu.py',
    'tokenizar_conllu.py',
    'udpipe_vertical.py',
    'estrutura_dados.py',
    'confusão.py',
    'conll18_ud_eval.py',
    'acdc-ud.md',
]

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
		for arquivo in lista_arquivos:
		    if os.path.isfile(arquivo): os.remove(arquivo)
		Git().checkout('master')

atualizar()
