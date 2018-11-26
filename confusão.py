# -*- coding: utf-8 -*-

import sys
from estrutura_dados import LerUD
import re
import os

try:
        import pandas as pd
except:
        try:
                from pip import main as pipmain
        except:
                print('Instale a biblioteca "pandas" e tente novamente.')
                exit()
        else:
                pipmain(['install', 'pandas'])
                print('Biblioteca "pandas" instalada com sucesso!')
                exit()

feats = {
                1: "ID",
                2: "FORM",
                3: "LEMMA",
                4: "UPOSTAG",
                5: "XPOSTAG",
                6: "FEATS",
                7: "HEAD",
                8: "DEPREL",
                9: "DEPS",
                10: "MISC",
}

def get_list(conllu1, conllu2, coluna):
        lista_coluna1 = list()
        lista_coluna2 = list()
        solitários1 = list()
        solitários2 = list()

        #Sentença por sentença do conllu1
        for sentença in conllu1:
                sentença_length = 0
                for linha in sentença:
                        #Encontrou o text_header da sentença
                        if '# text = ' in linha:
                                text_header = linha
                        #Cresce o tamanho de tokens da sentença
                        if isinstance(linha, list):
                                sentença_length += 1
                #Começa a alinhar com o conllu2 para ver se a sentença também tem lá
                tem = False
                for subsentença in conllu2:
                        sentença_correta = False
                        subsentença_length = 0
                        for sublinha in subsentença:
                                #Encontrou a sentença cujo text_header é igual
                                if sublinha == text_header:
                                        sentença_correta = True
                                #Cresceu o tamanho de tokens da sentença correta
                                if sentença_correta and isinstance(sublinha, list):
                                        subsentença_length += 1
                        #Se tiver uma sentença igual em text_header e em tamanho, tem = True
                        if sentença_correta and subsentença_length == sentença_length:
                                tem = True
                                for sublinha in subsentença:
                                    if isinstance(sublinha, list):
                                        lista_coluna2.append(sublinha[coluna-1])
                #Se encontrou sentença igual em conllu2, append!
                if tem:
                        for linha in sentença:
                                if isinstance(linha, list):
                                        lista_coluna1.append(linha[coluna-1])
                #Se não encontrou, solitários.append
                else:
                        solitários1.append(text_header)

        #Procurar os solitários2
        for sentença in conllu2:
                sentença_length = 0
                for linha in sentença:
                        if '# text =' in linha:
                                text_header = linha
                        if isinstance(linha, list):
                                sentença_length += 1
                tem = False
                for subsentença in conllu1:
                        sentença_correta = False
                        subsentença_length = 0
                        for sublinha in subsentença:
                                if sublinha == text_header:
                                        sentença_correta = True
                                if sentença_correta and isinstance(sublinha, list):
                                        subsentença_length += 1
                        if sentença_correta and subsentença_length == sentença_length:
                                tem = True
                if not tem:
                        solitários2.append(text_header)

        return {'matriz_1': lista_coluna1, 'matriz_2': lista_coluna2, 'solitários_1': solitários1, 'solitários_2': solitários2}


def gerar_HTML(matriz, ud1, ud2, col, output, codificação):
        html = ['<meta charset="'+codificação+'" \>','<body style="background-color:#CEF6CE">']#;font-family:Courier New
        html.append('<a id="topo"><h3>' + matriz.split('\n\n')[0] + '</h3></a><hr><h1>Confusão</h1><pre>')

        tiposy = dict()
        tiposx = dict()
        for i, linha in enumerate("\n".join(matriz.split('\n\n')[1:]).split('#!$$')[0].split('\n')[2:-1]):
                tiposy[i+2] = linha.split(' ')[0]
        for i, coluna in enumerate("\n".join(matriz.split('\n\n')[1:]).split('#!$$')[0].split('\n')[0].split()[1:-1]):
                tiposx[i+1] = coluna
        y = 0
        for linha in "\n".join(matriz.split('\n\n')[1:]).split('#!$$')[0].split('\n'):
                if linha.strip() != '':
                        linha_html = linha.split(' ')[0]
                        if y == 0 or y == 1:
                                for x, coluna in enumerate(linha.split()[1:]):
                                        linha_html += '&#09;' + coluna
                                y += 1
                        elif y < len(tiposy):
                                for x, coluna in enumerate(linha.split()[1:-1]):
                                        linha_html += '&#09;' + '<a href="' + output + '_html/' + tiposy[y] + '-' + tiposx[x+1] + '.html">' + coluna + '</a>'
                                y += 1
                                linha_html += '&#09;' + linha.split()[-1]
                        elif y == len(tiposy):
                                for x, coluna in enumerate(linha.split()[1:]):
                                        linha_html += '&#09;' + coluna
                        html.append(linha_html)
        html.append('</pre>')

        solitários = dict()
        for i, grupo in enumerate(matriz.split('#!$$')[1:]):
                grupo = [x for x in grupo.splitlines() if x]
                html.append('<b>' + grupo[0] + ' (' + str(len(grupo[1:])) + ''')</b> <input type="button" id="botao''' + str(i) + '''" value="Mostrar" onClick="ativa('solitary''' + str(i) + '''', 'botao''' + str(i) + '''')"><br>''')
                html.append("<div id='solitary" + str(i) + "' style='display:none'>")
                for linha in grupo[1:]:
                        if linha.strip() != '':
                                html.append(linha)
                html.append("</div>")

        sentenças = dict()
        for sentença in ud1:
                sentença_id = ''
                tamanho_sentença = 0
                for linha in sentença:
                        if '# text = ' in linha:
                                sentença_header = linha
                        if '# sent_id = ' in linha:
                                sentença_id = linha
                        if isinstance(linha, list):
                                tamanho_sentença += 1
                for subsentença in ud2:
                        subsentença_correta = False
                        tamanho_subsentença = 0
                        for sublinha in subsentença:
                                if '# text = ' in sublinha and sublinha == sentença_header:
                                        subsentença_correta = True
                                if sentença_id == '' and '# sent_id = ' in sublinha:
                                        sentença_id = sublinha
                                if isinstance(sublinha, list):
                                        tamanho_subsentença += 1
                        if subsentença_correta and tamanho_sentença == tamanho_subsentença:
                                sentença_limpo = [x for x in sentença if isinstance(x, list)]
                                subsentença_limpo = [x for x in subsentença if isinstance(x, list)]
                                sentença_limpo_string = [x for x in sentença if isinstance(x, list)]
                                subsentença_limpo_string = [x for x in subsentença if isinstance(x, list)]
                                for l, linha in enumerate(sentença_limpo_string):
                                        if isinstance(linha, list):
                                                sentença_limpo_string[l] = "&#09;".join(sentença_limpo_string[l])
                                sentença_limpo_string = "\n".join(sentença_limpo_string)
                                for l, linha in enumerate(subsentença_limpo_string):
                                        if isinstance(linha, list):
                                                subsentença_limpo_string[l] = "&#09;".join(subsentença_limpo_string[l])
                                subsentença_limpo_string = "\n".join(subsentença_limpo_string)
                                for k in range(len(sentença_limpo)):
                                        coluna1 = sentença_limpo[k][col-1]
                                        coluna2 = subsentença_limpo[k][col-1]
                                        palavra = sentença_limpo[k][1]
                                        if not coluna1 + '-' + coluna2 in sentenças:
                                                sentenças[coluna1 + '-' + coluna2] = [(sentença_id, re.sub(r'\b(' + re.escape(palavra) + r')\b', '<b>' + palavra +'</b>', sentença_header), sentença_limpo_string.replace("&#09;".join(sentença_limpo[k]), '<b>' + "&#09;".join(sentença_limpo[k]) + '</b>'), subsentença_limpo_string.replace("&#09;".join(subsentença_limpo[k]), '<b>' + "&#09;".join(subsentença_limpo[k]) + '</b>'))]
                                        else: sentenças[coluna1+'-'+coluna2].append((sentença_id, re.sub(r'\b(' + re.escape(palavra) + r')\b', '<b>' + palavra + '</b>', sentença_header), sentença_limpo_string.replace("&#09;".join(sentença_limpo[k]), '<b>' + "&#09;".join(sentença_limpo[k]) + '</b>'), subsentença_limpo_string.replace("&#09;".join(subsentença_limpo[k]), '<b>' + "&#09;".join(subsentença_limpo[k]) + '</b>')))

        open(output + '.html', 'w', encoding=codificação).write("<br>".join(html).replace('\n','<br>') + '''</body><script>
                                       function ativa(nome, botao){
                                       var div = document.getElementById(nome)
                                       if (div.style.display == 'none') {
                                       document.getElementById(botao).value='Esconder'
                                       div.style.display = 'block'
                                       } else {
                                       div.style.display = 'none'
                                       document.getElementById(botao).value='Mostrar'
                                       }
                                       }
                                       </script>''')

        #Páginas independentes
        for combinação in sentenças:
                html = ['<meta charset="'+codificação+'" \>','<body style="background-color:#CEF6CE">']
                html.append('<a id="topo"><h3>' + matriz.split('\n\n')[0] + '</h3></a><hr><h3><a href="../' + output + '.html">Voltar</a></h3>Dica: Para salvar o estado da página, <u>Ctrl+S</u> (Firefox).')
                if not os.path.isdir(output + '_html'):
                        os.mkdir(output + '_html')
                html.append('<h1><a id="' + combinação + '">' + combinação + '</a> (' + str(len(sentenças[combinação])) + ')</h1>')
                for i, sentença in enumerate(sentenças[combinação]):
                        html.append(str(i+1) + ' / ' + str(len(sentenças[combinação])) + '<br>' + sentença[0] + '<br>' + sentença[1] + '<br><br>' + combinação.split('-')[0] + ': <input type="checkbox" id="check" value="Selecionar"> ' + combinação.split('-')[1] + ': <input type="checkbox" id="check" value="Selecionar"> Comentários: <input type="text">')
                        html.append('''<br><input type="button" id="botao1''' + combinação + str(i) + '''" value="Mostrar UD[1]" onClick="ativa1('sentence1''' + combinação + str(i) + '''', 'botao1''' + combinação + str(i) + '''')"> <input type="button" id="botao2''' + combinação + str(i) + '''" value="Mostrar UD[2]" onClick="ativa2('sentence2''' + combinação + str(i) + '''', 'botao2''' + combinação + str(i) + '''')">''')
                        html.append("<div id='sentence1" + combinação + str(i) + "' style='display:none'><pre><b><br>UD[1]:</b><br>")
                        html.append(sentença[2] + "</pre></div><div id='sentence2" + combinação + str(i) + "' style='display:none'><pre><b><br>UD[2]:</b><br>")
                        html.append(sentença[3] + '</pre></div><br><hr>')
                open(output + '_html/' + combinação + '.html', 'w', encoding=codificação).write("<br>".join(html).replace('\n','<br>') + '''Dica: Para salvar o estado da página, <u>Ctrl+S</u> (Firefox).<h3><a href="../''' + output + '''.html">Voltar</a></h3></body><script>
                                                                      function ativa1(nome, botao){
                                                                      var div = document.getElementById(nome)
                                                                      if (div.style.display == 'none') {
                                                                      document.getElementById(botao).value='Esconder UD[1]'
                                                                      div.style.display = 'block'
                                                                      } else {
                                                                      div.style.display = 'none'
                                                                      document.getElementById(botao).value='Mostrar UD[1]'
                                                                      }
                                                                      }
                                                                      function ativa2(nome, botao){
                                                                      var div = document.getElementById(nome)
                                                                      if (div.style.display == 'none') {
                                                                      document.getElementById(botao).value='Esconder UD[2]'
                                                                      div.style.display = 'block'
                                                                      } else {
                                                                      div.style.display = 'none'
                                                                      document.getElementById(botao).value='Mostrar UD[2]'
                                                                      }
                                                                      }
                                                                      </script>''')

def main(ud1, ud2, output, coluna):
	conllu1 = LerUD(ud1)
	conllu2 = LerUD(ud2)
	lista_conllu = get_list(conllu1, conllu2, coluna)
	lista_conllu1 = lista_conllu['matriz_1']
	lista_conllu2 = lista_conllu['matriz_2']
	pd.options.display.max_rows = None
	pd.options.display.max_columns = None
	pd.set_option('display.expand_frame_repr', False)
	saída = list()
	saída.append('Col ' + str(coluna)+': ' + feats[coluna])
	saída.append('UD[1]: ' + ud1)
	saída.append('UD[2]: ' + ud2 + '\n')
	saída.append(str(pd.crosstab(pd.Series(lista_conllu1), pd.Series(lista_conllu2), rownames=['UD[1]'], colnames=['UD[2]'], margins=True)))
	saída.append('\n')
	saída.append('#!$$ Sentenças de UD[1] que não foram encontradas em UD[2]:\n')
	for item in lista_conllu['solitários_1']:
	        saída.append(item)
	saída.append('\n#!$$ Sentenças de UD[2] que não foram encontradas em UD[1]:\n')
	for item in lista_conllu['solitários_2']:
	        saída.append(item)

        #Output
	if ':' in output: codificação_saída = output.split(':')[1]
	else: codificação_saída = 'utf8'
	output = output.split(':')[0]

        #Gera os arquivos HTML
	gerar_HTML("\n".join(saída), conllu1, conllu2, coluna, output, codificação_saída)
	#Gera o arquivo "txt" (apenas a matriz)
	open(output, 'w', encoding=codificação_saída).write("\n".join(saída))

if __name__ == '__main__':
    número_de_argumentos_mínimo = 4

    if len(sys.argv) < número_de_argumentos_mínimo +1:
        print('uso: confusão.py ud1.conllu:utf8 ud2.conllu:utf8 saída.txt:utf8 coluna')
        print('Colunas:')
        for i in range(len(feats)):
                print(str(i+1) + ': ' + feats[i+1])
    elif len(sys.argv) >= número_de_argumentos_mínimo +1:
        main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    else:
        print('Argumentos demais')
