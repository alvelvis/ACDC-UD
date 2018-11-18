# ACDC-UD

Pacote de ferramentas em [Python 3](https://www.python.org/download/releases/3.0/) de conversão do AC/DC ([http://www.linguateca.pt/ACDC](http://www.linguateca.pt/ACDC)) para UD ([http://universaldependencies.org/](http://universaldependencies.org/)), e vice versa.

**Conteúdo:**

* [acdc_procura.py](#acdc_procurapy)
* [comparar_UD.py](#comparar_UDpy)
* [revisar_UD.py](#revisar_UDpy)
* [limpar_conllu.py](#limpar_conllupy)
* [tokenizar_conllu.py](#tokenizar_conllupy)
* [udpipe_vertical.py](#udpipe_verticalpy)
* [atualizar_repo.py](#atualizar_repopy)

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

    >> python3 acdc-procura.py acdc.html:utf8 ud.conllu:utf8 saída.conllu:utf8 --critério <parâmetros>

1) **acdc.html** é o código fonte da página de resultados do AC/DC. Você pode salvar o código fonte em um *.txt*, manualmente, ou simplesmente salvar a página *.html*

2) **ud.conllu** é o arquivo no formato Universal Dependencies que será modificado (ele deve conter as sentenças da página AC/DC)

3) **saída.conllu** é o arquivo que será gerado com as modificações requisitadas

**Parâmetros:**

    --critério <tipo> <parâmetros>
    O critério para modificação do arquivo UD
    Veja os critérios na seção a seguir

    --palavra-negrito <índice>
    Qual a palavra que deverá ser procurada no UD entre as palavras da expressão em negrito no AC/DC
    padrão: 0 (a primeira palavra)

    --não-marcar
    Caso o parâmetro não seja fornecido, toda substituição será seguida pelo identificador "!$", de modo que seja fácil encontrar no arquivo SAÍDA.conllu as alterações feitas

**Critérios de substituição:**

Tipo 1: Procurar por palavras no UD que apontem para a palavra em negrito no ACDC e substituir a coluna X, se Y, por Z

    exemplo: --critério 1 7#ccomp#ccomp:parataxis
    explicação: se a sexta coluna (índice 7) da palavra do UD que aponta para a palavra em negrito no ACDC estiver preenchida com a palavra "ccomp", vira "ccomp:parataxis"
    X = 7
    Y = ccomp
    Z = ccomp:parataxis

# comparar_UD.py

Com esse código é possível comparar dois arquivos *.conllu*, formato UD, e buscar sentenças cujas anotações sejam diferentes.

No final do arquivo de comparação, logo após o identificador "#!$$", ficarão registradas as sentenças que estejam presentes em um dos arquivos, mas não no outro.

Caso deseje revisar um arquivo UD a partir das diferenças entre dois arquivos, você pode fazer alterações nas linhas do arquivo de comparação que não contenham "-->" (identificador de discrepância) e, posteriormente, rodar o [revisar_UD.py](#revisar_UDpy) para deixar apenas as alterações feitas nas outras linhas.

## Exemplo

Depois de rodar o [acdc_procura.py](#acdc_procurapy), alguns tokens de algumas sentenças, que tinham o valor "ccomp" na coluna 7, tiveram essa mesma coluna substituida por "ccomp:parataxis". Ao comparar o arquivo original e o novo, teremos um novo arquivo com todas as sentenças em que essa alteração foi realizada, havendo destaque para a alteração em si com uma seta "-->".

Abaixo, um exemplo de sentença ao se comparar o arquivo original com o novo:

    # text = «Normalmente nós utilizamos dados históricos sobre a produtividade em cada região, além de informações de agricultores», diz.
    1	«	«	PUNCT	_	_	4	punct	_	SpaceAfter=No
    2	Normalmente	normalmente	ADV	_	_	4	advmod	_	_
    3	nós	nós	PRON	_	Case=Nom|Gender=Unsp|Number=Plur|Person=1|PronType=Prs	4	nsubj	_	_
    4	utilizamos	utilizar	VERB	_	Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin	21	ccomp	_	_
    --> 4	utilizamos	utilizar	VERB	_	Mood=Ind|Number=Plur|Person=1|Tense=Pres|VerbForm=Fin	21	ccomp:parataxis!$	_	_
    5	dados	dado	NOUN	_	Gender=Masc|Number=Plur	4	obj	_	_
    6	históricos	histórico	ADJ	_	Gender=Masc|Number=Plur	5	amod	_	_
    7	sobre	sobre	ADP	_	_	9	case	_	_
    8	a	o	DET	_	Definite=Def|Gender=Fem|Number=Sing|PronType=Art	9	det	_	_
    9	produtividade	produtividade	NOUN	_	Gender=Fem|Number=Sing	5	nmod	_	_
    10	em	em	ADP	_	_	12	case	_	_
    11	cada	cada	DET	_	Gender=Fem|Number=Sing|PronType=Tot	12	det	_	_
    12	região	região	NOUN	_	Gender=Fem|Number=Sing	9	nmod	_	SpaceAfter=No
    13	,	,	PUNCT	_	_	16	punct	_	_
    14	além	além	ADV	_	_	16	cc	_	MWE=além_de
    15	de	de	ADP	_	_	16	case	_	_
    16	informações	informação	NOUN	_	Gender=Fem|Number=Plur	9	conj	_	_
    17	de	de	ADP	_	_	18	case	_	_
    18	agricultores	agricultor	NOUN	_	Gender=Masc|Number=Plur	16	nmod	_	SpaceAfter=No
    19	»	»	PUNCT	_	_	4	punct	_	SpaceAfter=No
    20	,	,	PUNCT	_	_	9	punct	_	_
    21	diz	dizer	VERB	_	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	0	root	_	SpaceAfter=No
    22	.	.	PUNCT	_	_	21	punct	_	_

Note que a versão do arquivo novo está logo após uma seta "-->", enquanto que a do arquivo original está acima da alteração.

Caso as linhas com seta sejam as corretas, ele pode alterar as linhas "oficiais", sem seta, para deixá-las iguais às com setas e, posteriormente, rodar o [revisar_UD.py](#revisar_UDpy) para deixar apenas as alterações feitas na revisão.

## Como usar

    >> python3 comparar_UD.py ud1.conllu:utf8 ud2.conllu:utf8 saída.txt:utf8 <parâmetros>

**Parâmetros:**

    --com-info
    caso esse parâmetro não seja fornecido, o programa, ao comparar, irá remover das sentenças as linhas de informação, como "# sent_id" e "# source", para que não sejam encaradas como diferenças arquivos que venham de fontes diferentes, por exemplo

# revisar_UD.py

Com esse código, é possível apagar as marcas de comparação de um arquivo gerado a partir do programa [comparar_UD.py](#comparar_UDpy). Desse modo, o usuário pode comparar dois arquivos UD para revisar qual está certo, corrigir a partir da observação das setas ('-->'), e deixar apenas as alterações feitas.

## Exemplo

Observe a seguinte sentença gerada pelo [comparar_UD.py](#comparar_UDpy):

    # text = Gosto de levar a sério o meu papel de consultor encartado.
    1	Gosto	gosto	NOUN	_	Gender=Masc|Number=Sing	0	root	_	_
    2	de	de	ADP	_	_	3	mark	_	_
    3	levar	levar	VERB	_	VerbForm=Inf	1	acl	_	_
    4	a	o	ADP	_	_	5	case	_	_
    --> 4	a	a	ADP	_	_	5	case	_	_
    5	sério	sério	NOUN	_	Gender=Masc|Number=Sing	3	obl	_	_
    6	o	o	DET	_	Definite=Def|Gender=Masc|Number=Sing|PronType=Art	8	det	_	_
    7	meu	meu	DET	_	Gender=Masc|Number=Sing|PronType=Prs	8	det	_	_
    8	papel	papel	NOUN	_	Gender=Masc|Number=Sing	3	obj	_	_
    9	de	de	ADP	_	_	10	case	_	_
    10	consultor	consultor	NOUN	_	Gender=Masc|Number=Sing	8	nmod	_	_
    11	encartado	encartar	VERB	_	Gender=Masc|Number=Sing|VerbForm=Part	10	acl	_	_
    12	.	.	PUNCT	_	_	1	punct	_	_

O token 4, para um dos arquivos de comparação, teria como lema "o"; para o outro, "a". Caso eu queira manter como "o", basta deixá-lo assim e rodar o **revisar_UD.py**, que então a versão com seta ('-->') será apagada. Caso eu queira aceitar a resposta da seta de que o correto é "a", posso alterar o lema de "o" para "a" diretamente nesse arquivo de comparação. Desse modo, quando o script de revisão for executado, as linhas com seta serão apagadas, e permanecerá a versão que editei: "a".

## Como usar

    >> python3 revisar_UD.py comparação.conllu:utf8 revisado.conllu:utf8
    
O arquivo *comparação.conllu* deverá ser aquele que veio como resultado do [comparar_UD.py](#comparar_UDpy), tendo já sido revisado. O arquivo *revisado.conllu* será o resultado final, sem as setas da comparação.

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

    >> python3 limpar-conllu.py ud.conllu:utf8 texto.txt:utf8

A codificação é opcional, sendo o padrão *utf8*.

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

    >> python3 tokenizar_conllu.py ud.conllu tokenizado.conllu

# udpipe_vertical.py

Com esse script é possível rodar o UDPipe em um arquivo já tokenizado verticalmente pelo código [tokenizar_conllu.py](#tokenizar_conllupy).

## Como usar

    >> python3 udpipe_vertical.py modelo.udpipe tokenizado.conllu resultado.conllu

# atualizar_repo.py

Com esse código, você pode atualizar todas as ferramentas de conversão diretamente deste repositório.

## Como usar

    >> python3 atualizar_repo.py

Repare que, caso você não tenha alguma biblioteca instalada, ele instalará automaticamente e você terá de reiniciar o código.

Importante possuir instalado "python3-pip":

    $ sudo apt install python3-pip
