tabela = {	'yellow': '#FF4500',
			'purple': 'purple',
			'blue': 'blue',
			'red': 'red',
			'cyan': 'cyan',
}

def tudo(html, lista_ocorrencias):

	html1 = html.split('//TUDO')[0]
	html2 = html.split('//TUDO')[1]
	for i, ocorrencia in enumerate(lista_ocorrencias):
		html1 += 'if (document.getElementById("checkbox_'+str(i+1)+'")) {\n if (event == "marcar") {\n document.getElementById("checkbox_'+str(i+1)+'").checked = true \n} if (event == "desmarcar") {\n document.getElementById("checkbox_'+str(i+1)+'").checked = false \n} \n}\n'
		html1 += 'if (document.getElementById("mostrar_'+str(i+1)+'")) {\n if (event == "abrir") {\n if (document.getElementById("mostrar_'+str(i+1)+'").value == "Mostrar anotação") {\n document.getElementById("mostrar_'+str(i+1)+'").click() \n} \n} if (event == "fechar") {\n if (document.getElementById("mostrar_'+str(i+1)+'").value == "Esconder anotação") {\n document.getElementById("mostrar_'+str(i+1)+'").click() \n} \n} \n}'

	html = html1 + html2

	return html
