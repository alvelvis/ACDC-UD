# ACDC-UD

Pacote de ferramentas em [Python 3](https://www.python.org/download/releases/3.0/) de conversão do AC/DC ([http://www.linguateca.pt/ACDC](http://www.linguateca.pt/ACDC)) para UD ([http://universaldependencies.org/](http://universaldependencies.org/)), e vice versa.

* [Mapa conceitual](acdc-ud.md)

**Conteúdo:**

* [interrogar_UD.py](#interrogar_UDpy)
* [acdc_procura.py](#acdc_procurapy)
* [comparar_UD.py](#comparar_UDpy)
* [revisar_UD.py](#revisar_UDpy)
* [confusão.py](#confusãopy)
* [limpar_conllu.py](#limpar_conllupy)
* [tokenizar_conllu.py](#tokenizar_conllupy)
* [udpipe_vertical.py](#udpipe_verticalpy)
* [generate_release.py](#generate_releasepy)
* [split_conllu.py](#split_conllupy)

# interrogar_UD.py
Com esse código é possível realizar pesquisas em arguivos UD de acordo com dois critérios: 1- expressão regular; 2- pesquisa especifica.

O script é utilizado no site: http://comcorhd.tronco.me/interrogar-ud/

## Exemplo

**1- Parâmetro: Expressão regular**

Se a expressão regular for encontrada em alguma sentença, retorná-la.

	Exemplo: '1 dizer.*\n.*PROPN'
	Retornar sentenças com o lema "dizer" seguido de um "PROPN".

**2- Parâmetros: A#B#C#D**

Se em uma sentença tiver um token marcado como A na coluna B e não tiver nenhum outro token com valor C na coluna D apontando para ele, retornar a sentença.

Dica: O parâmetro C aceita o operador lógico '|' (ou).

	Exemplo: '2 root#8#nsubj|csubj#8'
	Retornar sentenças em que o 'root' não tenha nenhum 'nsubj' ou 'csubj' apontando para ele.

[**↥ voltar ao topo**](#ACDC-UD)

# acdc_procura.py

Com esse código é possível, a partir do resultado de uma busca no AC/DC, realizar alterações em um arquivo UD (.conllu).

## Exemplo

No AC/DC, corpus Floresta, pesquisamos as ocorrências da seguinte palavra:

    [id="B.*" & sema="dizer_relatoDIRETO" & variante="BR"]

O AC/DC retorna 76 sentenças, por exemplo:

    id=481 cad="Caderno Especial" sec="nd" sem="94a": «Existem algumas opções de como fazer isso», **disse** Sérgio Amaral, chefe de gabinete do ministro Rubens Ricupero .

Agora queremos que, no arquivo BOSQUE.conllu (formato UD), essas 76 sentenças sejam alteradas caso sigam algumas condições.

Observe a mesma sentença acima, da página de pesquisa do AC/DC, no UD:

    # text = «Existem algumas opções de como fazer isso», disse Sérgio Amaral, chefe de gabinete do ministro Rubens Ricupero.
    # source = CETENFolha n=487 cad=Brasil sec=pol sem=94b
    # sent_id = CF487-3r
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

A condição de modificação, nesse exemplo, será que as palavras que, no UD, apontam para a palavra em negrito no AC/DC, e que tenham o tipo de relação "ccomp", recebam também o tipo "parataxis" (critério 1).

O token em negrito no AC/DC é "disse". No UD, como visto acima, ele é o token de número 11. A palavra que aponta para o número 11 (coluna 7) e tem o tipo de relação "ccomp" (coluna 8), no UD, é a palavra "Existem", token de número 2. Logo, ela deve receber o tipo de relação "ccomp:parataxis".

Resultado:

    2	Existem	existir	VERB	_	Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin	11	ccomp:parataxis!$	_	_

Repare no identificador "!$" após "ccomp:parataxis": ele serve para ajudar na revisão de todos os tokens alterados.

## Como usar

    $ python3 acdc-procura.py acdc.html:utf8 ud.conllu:utf8 saída.conllu:utf8 --critério <parâmetros>

1) **acdc.html** é o código fonte da página de resultados do AC/DC. Você pode salvar o código fonte em um *.txt*, manualmente, ou simplesmente salvar a página *.html*

2) **ud.conllu** é o arquivo no formato Universal Dependencies que será modificado (ele deve conter as sentenças da página AC/DC)

3) **saída.conllu** é o arquivo que será gerado com as modificações requisitadas

**Parâmetros:**

    --critério <tipo> <parâmetros>
    O critério para modificação do arquivo UD
    Veja os critérios na seção a seguir

    --palavra-negrito <índice>
    Qual a palavra que deverá ser procurada no UD entre as palavras da expressão em negrito no AC/DC
    padrão: 1 (a primeira palavra)

    --não-marcar
    Caso o parâmetro não seja fornecido, toda substituição será seguida pelo identificador "!$", de modo que seja fácil encontrar no arquivo SAÍDA.conllu as alterações feitas

**Critérios de substituição:**

Tipo 1: Procurar por palavras no UD que apontem para a palavra em negrito no ACDC e substituir a coluna X, se Y, por Z

    exemplo: --critério 1 8#ccomp#ccomp:parataxis
    explicação: se a oitava coluna da palavra do UD que aponta para a palavra em negrito no ACDC estiver preenchida com o valor "ccomp", vira "ccomp:parataxis"
    X = 8
    Y = ccomp
    Z = ccomp:parataxis

[**↥ voltar ao topo**](#ACDC-UD)

# comparar_UD.py

Com esse código é possível comparar dois ou mais arquivos *.conllu*, formato UD, e buscar sentenças cujas anotações sejam diferentes.

Caso deseje revisar um arquivo UD a partir das diferenças entre vários arquivos UD, veja [revisar_UD.py](#revisar_UDpy).

## Exemplo

Depois de rodar o [acdc_procura.py](#acdc_procurapy), alguns tokens de algumas sentenças, que tinham o valor "ccomp" na coluna 8, tiveram essa mesma coluna substituida por "ccomp:parataxis". Comparando o arquivo original com esse novo, além de uma nova versão etiquetada com um outro modelo derivado do Bosque, teremos como resultado um arquivo de comparação em que todas as diferenças serão destacadas com uma seta "-->" seguida pelo número do arquivo em que a diferença aparece, sendo \[2] = arquivo gerado a partir do [acdc_procura.py](#acdc_procurapy), e [3] = arquivo gerado com o novo modelo do UDPipe.

Abaixo, um exemplo de sentença ao se comparar os 3 arquivos:

    # text = «O importante é levantar bem o joelho, manter o ritmo e encostar o calcanhar no chão a cada movimento», diz.
    1	«	«	PUNCT	_	_	3	punct	_	SpaceAfter=No
    -->[3]	«	«	PUNCT	_	_	5	punct	_	_
    2	O	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	3	det	_	_
    3	importante	importante	ADJ	_	Gender=Masc|Number=Sing	25	ccomp	_	_
    -->[2]	importante	importante	ADJ	_	Gender=Masc|Number=Sing	25	ccomp:parataxis!$	_	_
    -->[3]	importante	importante	NOUN	_	Gender=Masc|Number=Sing	5	nsubj	_	_
    4	é	ser	AUX	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	3	cop	_	_
    -->[3]	é	ser	AUX	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	5	cop	_	_
    5	levantar	levantar	VERB	_	VerbForm=Inf	3	csubj	_	_
    -->[3]	levantar	levantar	VERB	_	VerbForm=Inf	25	ccomp	_	_
    6	bem	bem	ADV	_	_	5	advmod	_	_
    7	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	8	det	_	_
    8	joelho	joelho	NOUN	_	Gender=Masc|Number=Sing	5	obj	_	SpaceAfter=No
    -->[3]	joelho	joelho	NOUN	_	Gender=Masc|Number=Sing	5	obj	_	_
    9	,	,	PUNCT	_	_	10	punct	_	_
    -->[3]	,	,	PUNCT	_	_	5	punct	_	_
    10	manter	manter	VERB	_	VerbForm=Inf	5	conj	_	_
    -->[3]	manter	manter	VERB	_	VerbForm=Inf	5	xcomp	_	_
    11	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	12	det	_	_
    12	ritmo	ritmo	NOUN	_	Gender=Masc|Number=Sing	10	obj	_	_
    13	e	e	CCONJ	_	_	14	cc	_	_
    14	encostar	encostar	VERB	_	VerbForm=Inf	5	conj	_	_
    -->[3]	encostar	encostar	VERB	_	Number=Sing|Person=3|VerbForm=Inf	10	conj	_	_
    15	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	16	det	_	_
    16	calcanhar	calcanhar	NOUN	_	Gender=Masc|Number=Sing	14	obj	_	_
    17-18	no	_	_	_	_	_	_	_	_
    17	em	em	ADP	_	_	19	case	_	_
    18	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	19	det	_	_
    19	chão	chão	NOUN	_	Gender=Masc|Number=Sing	16	nmod	_	_
    -->[3]	chão	chão	NOUN	_	Gender=Masc|Number=Sing	14	obl	_	_
    20	a	a	ADP	_	_	22	case	_	_
    21	cada	cada	DET	_	Gender=Masc|Number=Sing|PronType=Tot	22	det	_	_
    22	movimento	movimento	NOUN	_	Gender=Masc|Number=Sing	14	obl	_	SpaceAfter=No
    -->[3]	movimento	movimento	NOUN	_	Gender=Masc|Number=Sing	19	nmod	_	_
    23	»	»	PUNCT	_	_	3	punct	_	SpaceAfter=No
    -->[3]	»	»	PUNCT	_	_	5	punct	_	_
    24	,	,	PUNCT	_	_	14	punct	_	_
    -->[3]	,	,	PUNCT	_	_	5	punct	_	_
    25	diz	dizer	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	0	root	_	SpaceAfter=No
    -->[3]	diz	dizer	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	0	root	_	_
    26	.	.	PUNCT	_	_	25	punct	_	_

Note que a versão do arquivo golden aparece sem setas, e as demais, com uma seta e o número do arquivo UD em que elas aparecem entre colchetes.

Caso não houvesse nenhuma discrepância entre os três arquivos, as sentenças seriam mostradas sem nenhuma seta.

Caso as linhas com seta sejam as corretas, você pode alterar as linhas "oficiais", sem seta, para deixá-las iguais às com setas e, posteriormente, rodar o [revisar_UD.py](#revisar_UDpy) para deixar apenas as alterações, sem as linhas com setas.

## Como usar

    $ python3 comparar_UD.py saída.conllu:utf8 ud1.conllu:utf8 ud2.conllu:utf8 ... udX.conllu:utf8 <parâmetros>

1) **saída.conllu** é o arquivo final de comparação, com as várias versões para todas as sentenças.

2) **ud1.conllu** é um dos arquivos de comparação. No caso de discrepância, ele será o considerado "mais importante", pois não virá com seta.

3) **ud2.conllu** é o segundo arquivo de comparação. Em caso de discrepância, ela será considerada "acidental", e por isso sua versão será representada com uma seta "-->[2]".

4) **udX.conllu** é o arquivo de número X de comparação. Sua versão será representada por "-->[X]".

No final do arquivo de comparação (**saída.conllu**), logo após o identificador "#!$$", ficarão registradas as sentenças que estejam presentes nos arquivos de comparação, mas não no arquivo principal.

**Parâmetros:**

* *--colunas:* indicar as colunas que você quer comparar. Exemplo: --colunas 1#2#5#8

[**↥ voltar ao topo**](#ACDC-UD)

# revisar_UD.py

Com esse código é possível apagar as marcas de comparação de um arquivo gerado a partir do programa [comparar_UD.py](#comparar_UDpy). Desse modo, o usuário pode revisar um arquivo UD corrigindo-o a partir da análise da comparação com outros arquivos.

## Exemplo

Observe a seguinte sentença gerada pelo [comparar_UD.py](#comparar_UDpy):

    # text = Gosto de levar a sério o meu papel de consultor encartado.
    1	Gosto	gostar	VERB	_	Mood=Ind|Number=Sing|Person=1|Tense=Pres|VerbForm=Fin	0	root	_	_
    -->[2]	Gosto	gosto	NOUN	_	Gender=Masc|Number=Sing	0	root	_	_
    -->[3]	Gosto	gosto	NOUN	_	Gender=Masc|Number=Sing	0	root	_	_
    2	de	de	ADP	_	_	3	mark	_	_
    3	levar	levar	VERB	_	VerbForm=Inf	1	xcomp	_	_
    -->[2]	levar	levar	VERB	_	VerbForm=Inf	1	acl	_	_
    -->[3]	levar	levar	VERB	_	VerbForm=Inf	1	acl	_	_
    4	a	a	ADP	_	_	5	case	_	MWE=a_sério
    -->[2]	a	o	ADP	_	_	5	case	_	_
    -->[3]	a	a	ADP	_	_	5	case	_	_
    5	sério	sério	NOUN	_	_	3	xcomp	_	_
    -->[2]	sério	sério	NOUN	_	Gender=Masc|Number=Sing	3	obl	_	_
    -->[3]	sério	sério	NOUN	_	Gender=Masc|Number=Sing	3	obl	_	_
    6	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	8	det	_	_
    7	meu	meu	DET	_	Gender=Masc|Number=Sing|PronType=Prs	8	det	_	_
    8	papel	papel	NOUN	_	Gender=Masc|Number=Sing	3	obj	_	_
    9	de	de	ADP	_	_	10	case	_	_
    10	consultor	consultor	NOUN	_	Gender=Masc|Number=Sing	8	nmod	_	_
    11	encartado	encartar	VERB	_	Gender=Masc|Number=Sing|VerbForm=Part	10	acl	_	SpaceAfter=No
    -->[2]  encartado	encartar	VERB	_	Gender=Masc|Number=Sing|VerbForm=Part	10	acl	_	_
    -->[3]	encartado	encartar	VERB	_	Gender=Masc|Number=Sing|VerbForm=Part	10	acl	_	_
    12	.	.	PUNCT	_	_	1	punct	_	_

O token 3 (levar), para o arquivo UD[1], teria como DEPREL (8a coluna) o valor "xcomp"; para o UD[2], "acl", e para o UD[3], também "acl".

* Caso eu queira manter como "xcomp", a versão do UD[1], basta deixá-lo assim e rodar o **revisar_UD.py**, que então as versões com seta serão apagadas.

* Caso eu queira aceitar a resposta do UD[2] e do UD[3], de que o correto é "acl", posso alterar a versão "xcomp" para "acl" diretamente nesse arquivo de comparação. Assim, quando o script de revisão for executado, as linhas com seta serão apagadas, e permanecerá a versão que editei: "acl".

## Como usar

    $ python3 revisar_UD.py comparação.conllu:utf8 revisado.conllu:utf8

1) **comparação.conllu** deverá ser aquele que veio como resultado do [comparar_UD.py](#comparar_UDpy), tendo já sido revisado.

2) **revisado.conllu** será o resultado final, sem as setas da comparação.

A codificação é opcional, sendo o padrão *utf8*.

[**↥ voltar ao topo**](#ACDC-UD)

# confusão.py

Com esse código é possivel gerar matrizes de confusão e relatórios de erro para quaisquer colunas de dois arquivos UD. Além disso, junto com o *conll18_ud_eval.py*, você tem acesso às métricas oficiais de comparação entre os dois arquivos.

## Exemplo

Ao comparar a coluna 4 (UPOSTAG) de dois arquivos gerados pelo UDPipe com modelos diferentes, teremos:

    Col 4: UPOSTAG
    UD[1]: UD-Bosque/teste_tokenizado_modelonovo.conllu
    UD[2]: UD-Bosque/teste_tokenizado_pretrained.conllu

    UD[2]  ADJ   ADP  ADV  AUX  CCONJ   DET  NOUN  NUM  PRON  PROPN  PUNCT  SCONJ  SYM  VERB  X    _    All
    UD[1]
    ADJ    414     0    0    1      0     0    13    0     1      1      0      0    0     5  0    0    435
    ADP      1  1637    4    0      2     2     0    0     0      0      0      0    0     0  0    0   1646
    ADV      0     0  361    0      0     1     2    0     1      1      0      0    0     1  0    0    367
    AUX      0     0    0  278      0     0     0    0     0      0      0      0    0     4  0    0    282
    CCONJ    0     0    0    0    201     0     0    0     0      0      0      0    0     0  0    0    201
    DET      0     1    1    0      0  1548     2    1     3      0      0      0    0     0  0    0   1556
    NOUN    11     0    5    0      0     0  1923    2     0      8      0      0    0     8  0    0   1957
    NUM      0     0    0    0      0     0     0  212     0      1      0      0    0     0  0    0    213
    PRON     0     0    0    0      0     2     0    0   310      0      0      1    0     0  0    0    313
    PROPN    0     0    0    0      0     2     9    0     0    884      0      0    0     2  0    0    897
    PUNCT    0     0    0    0      0     0     0    0     0      0   1343      0    0     0  0    0   1343
    SCONJ    0     0    0    0      0     0     0    0     2      0      0     89    0     0  0    0     91
    SYM      0     0    0    0      0     0     0    0     0      0      0      0   29     0  0    0     29
    VERB     9     1    0    7      0     1     6    0     0      0      0      0    0   841  0    0    865
    X        0     0    0    0      0     0     2    0     0      0      0      0    0     0  2    0      4
    _        0     0    0    0      0     0     0    0     0      0      0      0    0     0  0  741    741
    All    435  1639  371  286    203  1556  1957  215   317    895   1343     90   29   861  2  741  10940

Note que, caso em um dos arquivos uma das sentença não esteja presente no outro ou a tokenização esteja diferente, essa sentença não será computada para gerar a matriz de confusão. No final do arquivo, após o identificador "#!$$", você encontra as sentenças que não foram possíveis ser computadas.

Para computar uma sentença, não importa a ordem em que elas aparecem nos arquivos UD, mas sim que o tamanho de tokens seja igual e o metadado "# text", também.

Além da matriz de confusão, **confusão.py** gera um relatório de erros em HTML e as métricas oficiais de comparação. Você pode conferir um exemplo clicando [aqui](http://comcorhd.tronco.me/acdc-ud/matriz/teste.html).

## Como usar

    $ python3 confusão.py ud1.conllu:utf8 ud2.conllu:utf8 saída.txt:utf8 <coluna>

A codificação é opcional, sendo o padrão *utf8*.

**Colunas:**

    1: "ID"
    2: "FORM"
    3: "LEMMA"
    4: "UPOSTAG"
    5: "XPOSTAS"
    6: "FEATS"
    7: "HEAD"
    8: "DEPREL"
    9: "DEPS"
    10: "MISC"

[**↥ voltar ao topo**](#ACDC-UD)

# limpar_conllu.py

Com esse código é possível remover toda a anotação de um arquivo UD, deixando apenas o texto cru.

## Exemplo

No arquivo *.conllu* original, há a seguinte sentença:

    # text = Gosto de levar a sério o meu papel de consultor encartado.
    1	Gosto	gosto	NOUN	_	Gender=Masc|Number=Sing	0	root	_	_
    2	de	de	ADP	_	_	3	mark	_	_
    3	levar	levar	VERB	_	VerbForm=Inf	1	acl	_	_
    4	a	o	ADP	_	_	5	case	_	_
    5	sério	sério	NOUN	_	Gender=Masc|Number=Sing	3	obl	_	_
    6	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	8	det	_	_
    7	meu	meu	DET	_	Gender=Masc|Number=Sing|PronType=Prs	8	det	_	_
    8	papel	papel	NOUN	_	Gender=Masc|Number=Sing	3	obj	_	_
    9	de	de	ADP	_	_	10	case	_	_
    10	consultor	consultor	NOUN	_	Gender=Masc|Number=Sing	8	nmod	_	_
    11	encartado	encartar	VERB	_	Gender=Masc|Number=Sing|VerbForm=Part	10	acl	_	_
    12	.	.	PUNCT	_	_	1	punct	_	_

Após rodar o **limpar_conllu.py**, essa sentença se transformará em:

    Gosto de levar a sério o meu papel de consultor encartado.

## Como usar

    $ python3 limpar-conllu.py ud.conllu:utf8 texto.txt:utf8

A codificação é opcional, sendo o padrão *utf8*.

[**↥ voltar ao topo**](#ACDC-UD)

# tokenizar_conllu.py

Apaga as anotações de um arquivo *.conllu* mas mantém a tokenização vertical, de modo que seja possível rodar o UDPipe nele posteriormente (veja [udpipe_vertical.py](#udpipe_verticalpy)).

## Exemplo

Observe a seguinte sentença, de um arquivo *.conllu*:

    # text = Provoca em quem o ouve a sensação de que aquilo que diz, o diz da forma mais justa, se não da única forma justa.
    # sent_id = 19
    1	Provoca	provoca	NOUN	_	Gender=Fem|Number=Sing	0	root	_	_
    2	em	em	ADP	_	_	3	case	_	_
    3	quem	quem	PRON	_	Gender=Fem|Number=Sing|PronType=Rel	5	obl	_	_
    4	o	ele	PRON	_	Case=Acc|Gender=Masc|Number=Sing|Person=3|PronType=Prs	5	obj	_	_
    5	ouve	ouver	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	1	acl:relcl	_	_
    6	a	o	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	7	det	_	_
    7	sensação	sensação	NOUN	_	Gender=Fem|Number=Sing	5	nsubj	_	_
    8	de	de	ADP	_	_	15	mark	_	_
    9	que	que	SCONJ	_	_	15	mark	_	_
    10	aquilo	aquilo	PRON	_	Gender=Masc|Number=Sing|PronType=Dem	15	nsubj	_	_
    11	que	que	PRON	_	Gender=Masc|Number=Sing|PronType=Rel	12	nsubj	_	_
    12	diz	dizer	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	10	acl:relcl	_	_
    13	,	,	PUNCT	_	_	12	punct	_	_
    14	o	ele	PRON	_	Case=Acc|Gender=Masc|Number=Sing|Person=3|PronType=Prs	15	obj	_	_
    15	diz	dizer	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	7	acl	_	_
    16-17	da	_	_	_	_	_	_	_	_
    16	de	de	ADP	_	_	18	case	_	_
    17	a	o	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	18	det	_	_
    18	forma	forma	NOUN	_	Gender=Fem|Number=Sing	15	obl	_	_
    19	mais	mais	ADV	_	_	20	advmod	_	_
    20	justa	justo	ADJ	_	Gender=Fem|Number=Sing	18	amod	_	_
    21	,	,	PUNCT	_	_	27	punct	_	_
    22	se	se	SCONJ	_	_	27	mark	_	_
    23	não	não	ADV	_	Polarity=Neg	27	advmod	_	_
    24-25	da	_	_	_	_	_	_	_	_
    24	de	de	ADP	_	_	27	case	_	_
    25	a	o	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	27	det	_	_
    26	única	único	ADJ	_	Gender=Fem|Number=Sing	27	amod	_	_
    27	forma	forma	NOUN	_	Gender=Fem|Number=Sing	15	nsubj	_	_
    28	justa	justo	ADJ	_	Gender=Fem|Number=Sing	27	amod	_	_
    29	.	.	PUNCT	_	_	1	punct	_	_

Após a execução do **tokenizar_conllu.py**, ela se transformará em:

    # text = Provoca em quem o ouve a sensação de que aquilo que diz, o diz da forma mais justa, se não da única forma justa.
    Provoca	_	_	_	_	_	_	_	_	_
    em	_	_	_	_	_	_	_	_	_
    quem	_	_	_	_	_	_	_	_	_
    o	_	_	_	_	_	_	_	_	_
    ouve	_	_	_	_	_	_	_	_	_
    a	_	_	_	_	_	_	_	_	_
    sensação	_	_	_	_	_	_	_	_	_
    de	_	_	_	_	_	_	_	_	_
    que	_	_	_	_	_	_	_	_	_
    aquilo	_	_	_	_	_	_	_	_	_
    que	_	_	_	_	_	_	_	_	_
    diz	_	_	_	_	_	_	_	_	_
    ,	_	_	_	_	_	_	_	_	_
    o	_	_	_	_	_	_	_	_	_
    diz	_	_	_	_	_	_	_	_	_
    16-17-=da	_	_	_	_	_	_	_	_	_
    de	_	_	_	_	_	_	_	_	_
    a	_	_	_	_	_	_	_	_	_
    forma	_	_	_	_	_	_	_	_	_
    mais	_	_	_	_	_	_	_	_	_
    justa	_	_	_	_	_	_	_	_	_
    ,	_	_	_	_	_	_	_	_	_
    se	_	_	_	_	_	_	_	_	_
    não	_	_	_	_	_	_	_	_	_
    24-25-=da	_	_	_	_	_	_	_	_	_
    de	_	_	_	_	_	_	_	_	_
    a	_	_	_	_	_	_	_	_	_
    única	_	_	_	_	_	_	_	_	_
    forma	_	_	_	_	_	_	_	_	_
    justa	_	_	_	_	_	_	_	_	_
    .	_	_	_	_	_	_	_	_	_

Repare que alguns tokens, as MWEs, tiveram o número da tokenização misturado com a palavra em si. Isso ocorre para facilitar o trabalho do [udpipe_vertical.py](#udpipe_verticalpy), pois de outra forma ele não teria como adivinhar quais chunks são MWEs ou não.

## Como usar

    $ python3 tokenizar_conllu.py ud.conllu tokenizado.conllu

[**↥ voltar ao topo**](#ACDC-UD)

# udpipe_vertical.py

Com esse script é possível rodar o UDPipe em um arquivo já tokenizado verticalmente pelo código [tokenizar_conllu.py](#tokenizar_conllupy).

## Como usar

    $ python3 udpipe_vertical.py modelo.udpipe tokenizado.conllu resultado.conllu

[**↥ voltar ao topo**](#ACDC-UD)

# generate_release.py

A partir de um arquivo *.txt* com IDs de sentenças e uma pasta "documents" com arquivos CoNLLU, criar o arquivo *.conllu* unindo as sentenças na ordem em que os IDs aparecem no arquivo de texto.

## Como usar

    $ python3 generate_release.py

Você será interrogado sobre o caminho do arquivo de IDs. Basta arrastá-lo para o terminal.

Então, **generate_release.py** criará um arquivo *.conllu* com o mesmo nome do arquivo de IDs e na mesma pasta que ele, unindo as sentenças dos arquivos da pasta "documents" na ordem em que aparecem no arquivo de IDs.

# split_conllu.py

A partir de arquivos *train, dev e teste*, **split_conllu.py** gera uma pasta *documents* com os arquivos unitários retirados do metadado "sent_id".

## Como usar

    $ python3 split_conllu.py

Você será interrogado sobre o caminho do arquivo *.conllu*. Basta arrastar a pasta para o terminal.

Então, **split_conllu.py** criará uma pasta "documents" com todos os arquivos unitários retirados dos metadados "sent_id", na ordem das sentenças original.
