# ACDC-UD

Pacote de ferramentas em [Python 3](https://www.python.org/download/releases/3.0/) de conversão do AC/DC ([http://www.linguateca.pt/ACDC](http://www.linguateca.pt/ACDC)) para UD ([http://universaldependencies.org/](http://universaldependencies.org/)), e vice versa.

**Conteúdo:**

* [estrutura_ud.py](#estrutura_udpy)
* [interrogar_UD.py](#interrogar_UDpy)
* [limpar_conllu.py](#limpar_conllupy)
* [tokenizar_conllu.py](#tokenizar_conllupy)
* [udpipe_vertical.py](#udpipe_verticalpy)
* [generate_release.py](#generate_releasepy)
* [split_conllu.py](#split_conllupy)
* [tratar_conllu.py](#tratar_conllupy)

# estrutura_ud.py

O arquivo serve de base para os demais scripts, estruturando os dados provenientes de um arquivo no formato *.conllu*.

## Como carregar um corpus

```python
import estrutura_ud
corpus = estrutura_ud.Corpus(recursivo=True, sent_id=None, thread=False, encoding="utf-8")
corpus.load("arquivo.conllu")
```
Mude o caminho para arquivo *.conllu* no método `load()`, e caso julgue necessário, configure os parâmetros da classe `Corpus` da seguinte maneira:

* recursivo (boolean): configura se o corpus terá recursão, isto é, se cada token do corpus terá o atributo head_token, que corresponde ao pai sintático, e next_token e previous_token, que correspondem, respectivamente, ao token à direita e à esquerda de cada token. Caso não seja necessária a recursão, desligue o parâmetro para tornar a contrução do corpus mais veloz.

* sent_id (string): configure se o corpus carregará apenas uma única sentença do arquivo, tornando muito mais veloz o carregamento do corpus, já que carregará apenas uma sentença.

* thread (integer): configura o número de CPUs que serão responsáveis por carregar as sentenças do corpus.

* encoding (string): configura a codificação do corpus, como por exemplo "utf-8", "utf-16" ou "latin-1".

## Como é a estrutura de dados

Uma classe do tipo Corpus possui um dicionário `sentences` com o conjunto de sentenças do corpus, sendo a chave do dicionário o "# sent_id" da frase, e o valor, um objeto do tipo `sentence`. Os objetos do tipo `sentence` contêm uma lista chamada `tokens`, com objetos do tipo `token`, e cada token possui, pelo menos, os atributos abaixo, que são todos "strings":

```
id, word, lemma, upos, xpos, feats, dephead, deprel, deps, misc
```

e os seguintes atributos, que são do tipo `token` (caso a recursão esteja ativada):

```
head_token, next_token, previous_token
```

Todos os objetos mencionados possuem o método `to_str()` para unificar os atributos de uma forma legível, e o objeto Corpus possui o método `save()` para salvar o arquivo CoNLL-U após possíveis edições que o usuário tenha realizado.

## Exemplos

Dessa maneira, é possível realizar as buscas e atribuições abaixo:

```python
import estrutura_ud
corpus = estrutura_ud.Corpus()
corpus.load("arquivo.conllu")

print(corpus.to_str())
print(corpus.sentences["FRASE-1"].to_str())
print(corpus.sentences["FRASE-1"].tokens[0].to_str())
corpus.sentences["FRASE-1"].tokens[5].upos = "ADJ"
print(corpus.sentences["FRASE-1"].tokens[5].head_token.word)
corpus.sentences["FRASE-1"].tokens[5].head_token.upos = "NOUN"
corpus.save("arquivo.conllu")
```

[**↥ voltar ao topo**](#ACDC-UD)

# interrogar_UD.py

Com esse código é possível realizar pesquisas em arquivos UD de acordo com diferentes critérios.

O script é a base para o [Interrogatório, ambiente de busca e revisão de corpora anotados](http://github.com/alvelvis/Interrogat-rio).

Consule o repositório do Interrogatório para mais informações.

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

A partir de um arquivo *.txt* com IDs de sentenças e uma pasta "documents" com arquivos CoNLL-U, criar o arquivo *.conllu* unindo as sentenças na ordem em que os IDs aparecem no arquivo de texto.

## Como usar

    $ python3 generate_release.py <pasta com arquivos txt e pasta documents>

Você será interrogado sobre o caminho do arquivo de IDs. Basta arrastá-lo para o terminal, ou descrevê-lo na linha de comando do script.

Então, **generate_release.py** criará um arquivo *.conllu* com o mesmo nome do arquivo de IDs e na mesma pasta que ele, unindo as sentenças dos arquivos da pasta "documents" na ordem em que aparecem no arquivo de IDs.

[**↥ voltar ao topo**](#ACDC-UD)

# split_conllu.py

A partir de qualquer arquivo .conllu, **split_conllu.py** gera uma pasta *documents* com os arquivos unitários retirados do metadado "sent_id". O nome do arquivo será o sent_id antes do hífen, e, após o hífen, é esperado o número da sentença dentro do arquivo, por exemplo, ARQUIVO1-1, ARQUIVO1-2, ARQUIVO1-3, etc.

## Como usar

    $ python3 split_conllu.py <arquivo conllu>

Você será interrogado sobre o caminho do arquivo *.conllu*. Basta arrastar a pasta para o terminal ou indicá-lo na linha de comando.

Então, **split_conllu.py** criará uma pasta "documents" com todos os arquivos unitários retirados dos metadados "sent_id", na ordem das sentenças original.

[**↥ voltar ao topo**](#ACDC-UD)

# tratar_conllu.py

Trata os dados em um arquivo .conllu para servir de material de treino ao UDPipe.

O script remove as colunas XPOS e Misc, além de alguns cabeçalhos irrelevantes para o momento de treinamento.

## Como usar

    $ python3 tratar_conllu.py

Será requisitado que o usuário arraste o arquivo *.conllu* para o terminal.

[**↥ voltar ao topo**](#ACDC-UD)
