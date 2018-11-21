# ACDC-UD

  - acdc_procura.py

    - critérios
      em franca expansão!

      - [x] critério 1: Procurar por palavras no UD que apontem para a palavra em negrito no ACDC e substituir a coluna X, se Y, por Z

    - [x] ponto final nas sentenças do AC/DC: corrigido

    - [x] faz procuras apenas em código fonte do AC/DC (página web)
       talvez fosse interessante colocar também para arquivo fonte

      - [ ] NÚMERO DE OCORRÊNCIAS EXCESSIVO: como lidar?

  - conll18_ud_eval.py

    - [x] dá as métricas de comparação entre um arquivo "sistema" e "golden"

    - [x] sei utilizar: variável -v para todas as métricas, e não apenas as específicas do CONLL18

    - [x] possibilidade de alteração de algumas linhas de código!

  - atualizar_repo.py

    - [x] apaga todos os arquivos relevantes de uma determinada pasta

    - [x] clona o meu repositório sem conflitos, uma vez que os arquivos já foram apagados

  - udpipe_vertical.py

    - roda o udpipe em um arquivo conllu esvaziado, porém mantida a tokenização pelo tokenizar_conllu.py

      - [x] procura o metadado "# text = " no arquivo original

      - [x] procura as MWEs no arquivo original (gerado pelo tokenizar_conllu.py)

  - tokenizar_conllu.py

    - [x] retira toda anotação de um arquivo UD, porém mantendo a tokenização

    - ideal para pós-etiquetar com o UDPipe

      - [x] mantém os metadados "# text" para que o udpipe_vertical.py possa encontrar as sentenças sem tokenização

      - [x] mescla o ID das MWEs para que o udpipe_vertical.py possa encontrar as MWEs e zerar suas colunas

  - matriz_confusão.py

    - [x] gerar matriz de confusão a partir de dois arquivos UD

    - [x] qualquer coluna será comparada

    - [x] indica os dois arquivos em questão

    - [ ] RELATÓRIO DE ERROS

  - comparar_UD.py

    - [x] comparar dois ou mais arquivos UD

      - [x] uma seta para cada discrepância

    - [x] não importa a ordem das sentenças, mas que tenham a tokenização igual e o "# text" também

  - limpar_conllu.py

    - [x] retira toda a informação de um arquivo UD, deixando apenas as sentenças (informações após "# text = "

  - revisar_UD.py

    - [x] apagar as setas de um dado arquivo gerado a partir do comparar_UD.py

  - edição_lotes.py

    - luísa:

      - [ ] "Se o valor de uma coluna X for Y, mudar para Z"

  - README.me

    - [x] atualizado para cada código

    - [x] # Nome e definição

    - [x] ## Exemplo

    - [x] ## Como usar

      - [x] subcategorias, como **Critérios de substituição**

    - [x] voltar ao topo

