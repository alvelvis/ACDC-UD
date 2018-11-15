# ACDC-UD
Ferramentas de conversão do AC/DC ([http://www.linguateca.pt/ACDC](http://www.linguateca.pt/ACDC)) para UD e vice versa.

Conteúdo:

* [acdc-procura.py](#acdc-procura)
* [comparar-UD.py](#comparar-UD)
* [limpar-conllu.py](#limpar-conllu)
* [atualizar-repo.py](#atualizar-repo)

# acdc-procura

Com esse código é possível, a partir do resultado de uma busca no AC/DC, realizar alterações em um arquivo UD (.conllu).

## Exemplo

No AC/DC, corpus Floresta, quero as ocorrências da seguinte palavra:

    [id="B.*" & sema="dizer_relatoDIRETO" & variante="BR"]

O AC/DC retorna 76 sentenças, por exemplo:

    id=481 cad="Caderno Especial" sec="nd" sem="94a": «Existem algumas opções de como fazer isso», **disse** Sérgio Amaral, chefe de gabinete do ministro Rubens Ricupero .

Agora quero que, no arquivo BOSQUE.conllu (formato UD), essas 76 sentenças sejam alteradas caso sigam algumas condições.

Observe a mesma sentença acima, do AC/DC, no UD:

    # text = «Existem algumas opções de como fazer isso», disse Sérgio Amaral, chefe de gabinete do ministro Rubens Ricupero.
    # source = CETENFolha n=487 cad=Brasil sec=pol sem=94b
    # sent_id = CF487-3
    # id = 2053
    1	«	«	PUNCT	_	_	2	punct	_	SpaceAfter=No
    2	Existem	existir	VERB	_	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin	11	ccomp	_	_
    3	algumas	algum	DET	_	Gender=Fem|Number=Plur|PronType=Ind	4	det	_	_
    4	opções	opção	NOUN	_	Gender=Fem|Number=Plur	2	nsubj	_	_
    5	de	de	ADP	_	_	7	mark	_	_
    6	como	como	ADV	_	_	7	advmod	_	_
    7	fazer	fazer	VERB	_	VerbForm=Inf	4	acl	_	_
    8	isso	isso	PRON	_	Gender=Masc|Number=Sing|PronType=Dem	7	obj	_	SpaceAfter=No
    9	»	»	PUNCT	_	_	2	punct	_	SpaceAfter=No
    10	,	,	PUNCT	_	_	7	punct	_	_
    11	disse	dizer	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin	0	root	_	_
    12	Sérgio	Sérgio	PROPN	_	Gender=Masc|Number=Sing	11	nsubj	_	MWE=Sérgio_Amaral|MWEPOS=PROPN
    13	Amaral	Amaral	PROPN	_	Number=Sing	12	flat:name	_	SpaceAfter=No
    14	,	,	PUNCT	_	_	15	punct	_	_
    15	chefe	chefe	NOUN	_	Gender=Masc|Number=Sing	12	appos	_	_
    16	de	de	ADP	_	_	17	case	_	_
    17	gabinete	gabinete	NOUN	_	Gender=Masc|Number=Sing	15	nmod	_	_
    18-19	do	_	_	_	_	_	_	_	_
    18	de	de	ADP	_	_	20	case	_	_
    19	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	20	det	_	_
    20	ministro	ministro	NOUN	_	Gender=Masc|Number=Sing	17	nmod	_	_
    21	Rubens	Rubens	PROPN	_	Gender=Masc|Number=Sing	20	dep	_	MWE=Rubens_Ricupero|MWEPOS=PROPN
    22	Ricupero	Ricupero	PROPN	_	Number=Sing	21	flat:name	_	SpaceAfter=No
    23	.	.	PUNCT	_	_	11	punct	_	_
    
A condição de modificação é que as palavras que, no UD, apontam para a palavra em negrito no AC/DC, e que tenham o tipo de relação "ccomp", recebam também o tipo "parataxis".

O token em negrito no AC/DC é "disse". Aqui no UD, ele é o token de número 11. Quem aponta para o número 11 (coluna 7) e tem o tipo de relação "ccomp" (coluna 8), no UD, é a palavra "Existem", token de número 2.

Logo, ele deve receber o tipo de relação "parataxis". Resultado:

    2	Existem	existir	VERB	_	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin	11	ccomp parataxis	_	_
    
## Como usar

    acdc-procura.py ACDC.html UD.conllu SAÍDA.conllu <opcionais>
    
1) ACDC.html é o código fonte da página de resultados do AC/DC. Você pode salvar o código fonte em um *.txt* , manualmente, ou simplesmente salvar a página *.html*

2) UD.conllu é o arquivo no formato Universal Dependencies que será modificado (ele deve conter todas as sentenças da página AC/DC)

3) SAÍDA.conllu é o arquivo que será gerado com as modificações requisitadas

**Opcionais:**

* --cod-acdc <codificação> (a codificação do arquivo AC/DC --> padrão: utf8)
* --cod-ud <codificação> (a codificação do arquivo UD --> padrão: utf8)
* --cod-saída <codificação> (a codificação do arquivo de saída --> padrão: utf8)
* --palavra-negrito <índice> (da expressão em negrito, qual a palavra que deverá ser procurada no UD, começando pelo número 0 --> padrão: 0)
* --critério \<coluna>:<condição>:<substituição> (o critério para modificação do arquivo UD, sendo \<coluna> o item que deverá ser procurado, começando pelo número 0, <condição>, a palavra/número que deverá estar preenchido nessa coluna, e <substituição>, pelo que essa palavra/número será substituído(a))
* --não-marcar (caso o parâmetro não seja fornecido, toda substituição será seguida pelo identificado "#!$", de modo que seja fácil encontrar no arquivo SAÍDA as alterações feitas)
