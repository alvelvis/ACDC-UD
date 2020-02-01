import sys
import re
import estrutura_ud
import pprint

arquivo = sys.argv[1]

lista_tags = []
sentences = []
tokens = []
lista_faltantes = []
dep_lugar_errado = []
lista_contracoes = []
sent_id = 1
primeira_plus = False
ja_primeira_plus = False
MWE = False

dicionario_contracoes = {
    'No': 'Em+o',
    'pela': 'por+a',
    'dos': 'de+os',
    'da': 'de+a',
    'do': 'de+o',
    'na': 'em+a',
    'desse': 'de+esse',
    'ao': 'a+o',
    'à': 'a+a',
    'no': 'em+o',
    'num': 'em+um',
    'nesse': 'em+esse',
    'disso': 'de+isso',
    'daqui': 'de+aqui',
    'dali': 'de+ali',
    'das': 'de+os',
    'mo': 'me+o',
    'destas': 'de+estas',
    'naquela': 'em+aquela',
    'dele': 'de+ele',
    'pelo': 'por+o',
    'daí': 'de+aí',
    'delas': 'de+elas',
    'contigo': 'com+te',
    'Daqui': 'De+aqui',
    'às': 'a+as',
    'dela': 'de+ela',
    'àquela': 'a+aquela',
    'lho': 'lhe+o',
    'nestas': 'em+estas',
    'naquele': 'em+aquele',
    'nessa': 'em+essa',
    'pelos': 'por+os',
    'dessas': 'de+essas',
    'dessa': 'de+essa',
    'aos': 'a+os',
    'nas': 'em+as',
    'numa': 'em+uma',
    'À': 'A+a',
    'nos': 'em+os',
    'desses': 'de+esses',
    'nesta': 'em+esta',
    'Desta': 'De+esta',
    'nele': 'em+ele',
    'Na': 'Em+a',
    #'quais': 'quais',
    'deles': 'de+eles',
    'daquela': 'de+aquela',
    'Nesses': 'Em+esses',
    'comigo': 'com+mim',
    'nela': 'em+ela',
    'eilo': 'ei+o',
    'pelas': 'por+as',
    'daquele': 'de+aquele',
    #'qual': '',
    'desta': 'de+esta',
    'consigo': 'com+si',
    'Num': 'Em+um',
    'destes': 'de+estes',
    'naqueles': 'em+aqueles',
    'dentre': 'de+entre',
    'deste': 'de+este',
    'dantes': 'de+antes',
    'neste': 'em+este',
    'Nisto': 'Em+isto',
    'Nas': 'Em+as',
    'daqueles': 'de+aqueles',
    'Daí': 'De+aí',
    'Pelos': 'Por+os',
    'Nesse': 'Em+esse',
    'convosco': 'com+vos',
    'Às': 'A+as',
    'Neste': 'Em+este',
    'Da': 'De+a',
    #'em': '',
    #'paga': '',
    'nuns': 'em+uns',
    'Daquela': 'De+aquela',
    'daquelas': 'de+aquelas',
    'Doutras': 'De+outras',
    'pra': 'para+a',
    'Nessas': 'Em+essas',
    'Ao': 'A+o',
    'Aos': 'A+os',
    'naquilo': 'em+aquilo',
    'Do': 'De+o',
    'Eilo': 'Ei+o',
    'connosco': 'com+nos',
    'Nesta': 'Em+esta',
    'Naquela': 'Em+aquela',
    'Eilos': 'Ei+os',
    'lhos': 'lhe+os',
    'naquelas': 'em+aquelas',
    'nessas': 'em+essas',
    'nesses': 'em+esses',
    'àquele': 'a+aquele',
    'noutra': 'em+outra',
    'noutro': 'em+outro',
    'nisto': 'em+isto',
    'Dantes': 'De+antes',
    'nestes': 'em+estes',
    'ma': 'me+a',
    'Eila': 'Ei+a',
    'Das': 'De+as',
    'lhas': 'lhe+as',
    #'a': 'a',
    #'par': '',
    'pro': 'para+o',
    'Deste': 'De+estes',
    'àqueles': 'a+aqueles',
    'Comigo': 'Com+mim',
    'neles': 'em+eles',
    'Nessa': 'Em+essa',
    'Numa': 'Em+uma',
    'nisso': 'em+isso',
    'Naquele': 'Em+aquele',
    'to': 'te+o',
    'doutro': 'de+outro',
    'pras': 'para+as',
    'Nos': 'Em+os',
    'Pra': 'Para+a',
    'Pelo': 'Para+o',
    'Pela': 'Por+a',
    'Disto': 'De+isto',
    'numas': 'em+umas',
    'daquilo': 'de+aquilo',
    'àquelas': 'a+aquelas',
    'lha': 'lhe+a',
    'disto': 'de+isto',
    'Destes': 'De+estes',
    'Dessa': 'De+essa',
    'Contigo': 'Com+te',
    'Dentre': 'De+entre',
    'dalguma': 'de+alguma',
    'Dos': 'De+os',
    'Nele': 'Em+ele',
    'Pelas': 'Por+as',
    'àquilo': 'a+aquilo',
    'tos': 'te+os',
    'Nestes': 'Em+estes',
    'Disso': 'De+isso',
    'Noutras': 'Em+outras',
    'nalguma': 'em+alguma',
    'dum': 'de+um',
    'noutros': 'em+outros',
    'doutras': 'de+outras',
    'Desse': 'De+esse',
    'Destas': 'De+estas',
    'noutras': 'em+outras',
    'Daquele': 'De+aquele',
    'nelas': 'em+elas',
    'Dela': 'De+ela',
    'nalgum': 'em+algum',
    'nAS': 'em+as',
    'Dumas': 'De+umas',
    #'EM+A': '',
    #'DE+O': '',
    'Àquele': 'A+aquele',
    'Dele': 'De+ele',
    #'este+outro': '',
    'dalgum': 'de+algum',
    'duma': 'de+uma',
    'Dali': 'De+ali',
    'doutros': 'de+outros',
    'Desses': 'De+esses',
    'Nestas': 'Em+estas',
    #'DE+A': '',
    'Delas': 'De+elas',
    'eila': 'ei+ela',
    'AO': 'a+o',
    'Eilas': 'Ei+eças',
    #'DE+AS': '',
    'Àquela': 'A+aquela',
    #'com+o': '',
    'tas': 'te+as',
    #'EM+O': '',
    #'Me+a': '',
    #'Com+o': '',
    'Daqueles': 'De+aqueles',
    'Naqueles': 'Em+aqueles',
    'Pro': 'Para+o',
    'eilos': 'ei+os',
    #'DE+OS': '',
    'Naquelas': 'Em+aquelas',
    'Dum': 'De+um',
    #'com+a': '',
    #'esta+outra': '',
    'Dessas': 'De+essas',
    'Nelas': 'Em+elas',
    'ta': 'te+a',
    'Convosco': 'Com+vos',
    #'Com+a': '',
    #'sem': '',
    #'ofensa': '',
    'Doutro': 'De+outro',
    'Daquelas': 'De+aquelas',
    #'rumo': '',
    #'EM+AS': '',
    'Neles': 'Em+eles',
    'Nisso': 'Em+isso',
    'Nela': 'Em+eça',
    'AOS': 'A+os',
    'pros': 'para+os',
    'eilas': 'ei+as',
    'praí': 'para+aí',
    'dalguns': 'de+alguns',
    'dumas': 'de+umas',
    'Duma': 'De+uma',
    #'Te+a': '',
    'mos': 'me+os',
    #'POR+A': '',
    'Noutro': 'Em+outro',
    'dacolá': 'de+acolá',
    'doutra': 'de+outra',
    #'POR+O': '',
    'duns': 'de+uns',
    #'lume': '',
    #'dêstes+estes': '',
    #'dêsse+esse': '',
    #'dêste+este': '',
    #'dêsses+esses': '',
    'AAS': 'A+AS',
    'praqui': 'para+aqui',
    'nO': 'em+o',
    #'meado': '',
    'Nalguma': 'Em+alguma',
    'Deles': 'De+eles',
    'Numas': 'Em+umas',
    'Noutra': 'Em+outra',
    #'Te+o': '',
    #'aquela+outra': '',
    #'desabono': '',
    #'adonde': '',
    #'PARA+AS': '',
    'Pros': 'Para+os',
    #'DE+ANTES': '',
    'Noutros': 'Em+outros',
    'AA': 'A+A',
    #'DE+ESTA': '',
    #'A': '',
    #'DE+ELE': '',
    #'DE+AQUELE': '',
    #'EM+ISTO': '',
    #'EM+ESSA': '',
    #'DE+AQUELA': '',
    #'DE+UMAS': '',
    #'Adonde': '',
    'nalguns': 'em+alguns',
    'nalgumas': 'em+algumas',
    'Nalguns': 'Em+alguns',
    'Daquilo': 'De+aquilo',
    'Naquilo': 'Em+aquilo',
    #'EM+UMA': '',
    'dO': 'de+o',
}

try:
    with open(arquivo, encoding="utf-8") as f:
        corpus = f.read()#[:1000000]
except:
    with open(arquivo, encoding="latin-1") as f:
        corpus = f.read()

corpus_splitlines = corpus.splitlines()

if not corpus.startswith("#"):

    max_linhas = len(corpus_splitlines)
    for l, linha in enumerate(corpus_splitlines):

        try:

            if linha.strip().startswith("<obra "):
                obra = re.search('<obra id="([^"]+)"', linha)[1] if re.search('id="([^"]+?)"', linha) else "_INDEF_"
            if linha.strip().startswith("<tituloobra"):
                tituloobra = re.search('<tituloobra id="([^"]+)"', linha)[1] if re.search('id="([^"]+?)"', linha) else "_INDEF_"
            if linha.strip().startswith("<autor"):
                autor = re.search('<autor id="([^"]+)"', linha)[1] if re.search('id="([^"]+?)"', linha) else "_INDEF_"
            if linha.strip().startswith("<") and not linha.strip().startswith("<mwe") and not linha.strip().startswith("</mwe"):
                lista_tags.append(linha.replace("|", "\\|"))

            if linha.strip().startswith("<mwe"):
                MWE = True
                MWE_lema = re.search(r"lema=([^\s>]+)", linha)[1] if re.search(r"lema=([^\s>]+)", linha) else "_INDEF_"
                MWE_pos = re.search(r"pos=([^\s>]+)", linha)[1] if re.search(r"pos=([^\s>]+)", linha) else "_INDEF_"
            if linha.strip().startswith("</mwe"):
                MWE = False

            if len(linha.split("\t")) > 17:

                for i in range(len(linha.split("\t")[17].split("+"))):

                    if not linha.split("\t")[17].split("+")[i]:
                        lista_faltantes.append(ACDC.splitlines()[l-1] + "\n" + ACDC.splitlines()[l])
                        continue
                    if not '->' in linha.split("\t")[17]:
                        for coluna in linha.split("\t"):
                            if '->' in coluna:
                                dep_lugar_errado.append(linha)
                                nova_linha = linha.split("\t")
                                nova_linha[17] = coluna
                                linha = "\t".join(nova_linha)
                                break

                    if linha.split("\t")[0] in dicionario_contracoes and '+' in linha.split("\t")[17]:
                        word_or_plus = dicionario_contracoes[linha.split("\t")[0]].split("+")[i]
                    elif '-' in linha.split("\t")[0] and "+" in linha.split('\t')[17]:
                        word_or_plus = "+".join([dicionario_contracoes[x] if x in dicionario_contracoes else x for x in linha.split("\t")[0].replace("-", "+").split("+")]).split("+")[i]
                    else:
                        word_or_plus = linha.split("\t")[0]

                    misc = [f"{col}={x}" for col, x in enumerate(linha.split("\t")) if col not in [0,8,9,10,11,12,18,1,13,15,2,4,6]]
                    if any(corpus_splitlines[l+1].strip().startswith(x) for x in ["<"]):
                        misc.append("TAGAFTER=" + corpus_splitlines[l+1])
                    if any(corpus_splitlines[l-1].strip().startswith(x) for x in ["<"]):
                        misc.append("TAGB4=" + corpus_splitlines[l-1])

                    if '+' in linha.split("\t")[17]:
                        if (not primeira_plus and not ja_primeira_plus) or (i == 0):
                            primeira_plus = True
                    else:
                        primeira_plus = False
                        ja_primeira_plus = False                    

                    if primeira_plus:
                        tokens.append("{}-{}\t{}".format(linha.split("\t")[17].split("+")[i].split("->")[0].split("-")[0], int(linha.split("\t")[17].split("+")[i].split("->")[0].split("-")[0]) + len(linha.split("\t")[17].split("+"))-1, linha.split("\t")[0]) + ("\t_" * 8))
                        ja_primeira_plus = True
                        primeira_plus = False

                    tokens.append("{id}\t{word}\t{lemma}\t{upos}\t{xpos}\t{feats}\t{dephead}\t{deprel}\t{deps}\t{misc}".format(
                            id = linha.split("\t")[17].split("+")[i].split("->")[0].split("-")[0],
                            word = word_or_plus,
                            lemma = linha.split("\t")[8].split("+")[i] if '+' in linha.split("\t")[8] else linha.split("\t")[8],
                            upos = linha.split("\t")[9].split("+")[i] if '+' in linha.split("\t")[9] else linha.split("\t")[9],
                            xpos = linha.split("\t")[18].split("+")[i] if '+' in linha.split("\t")[18] else linha.split("\t")[18],
                            feats = "|".join([linha.split("\t")[10], linha.split("\t")[11], linha.split("\t")[12]]),
                            dephead = linha.split("\t")[17].split("+")[i].split("->")[1].split("-")[0],
                            deprel = linha.split("\t")[13].split("+")[i],
                            deps = linha.split("\t")[15],
                            misc = "|".join(misc) if not MWE else "|".join(sorted(misc + ["MWE=" + MWE_lema.replace("=", "_"), "MWEPOS=" + MWE_pos])),
                    ))

            if '</u>' in linha.strip():
                if l/max_linhas > 0.9 and not "\t" in "\n".join(corpus.splitlines()[l+1:]):
                    lista_tags.extend(corpus.splitlines()[l+1:])
                sentence = f"# sent_id = {obra.strip().replace(' ', '-')}-{sent_id}\n"
                sentence += f"# obra = {obra}\n"
                sentence += f"# tituloobra = {tituloobra}\n"
                sentence += f"# autor = {autor}\n"
                sentence += f"# xml_tags = {'|'.join(lista_tags)}\n"
                sentence += f'# text = ' + " ".join([x.split("\t")[1] for x in tokens if not '-' in x.split("\t")[0]]) + "\n"
                sentence += "\n".join(tokens)
                sentences.append(sentence)
                lista_tags = []
                tokens = []
                sent_id += 1

        except:
            raise Exception(linha)

    #ajeitando ID das MWEs
    corpus = estrutura_ud.Corpus()
    corpus.build("\n\n".join(sentences))

    for sentence in corpus.sentences.values():
        mapa_dephead = {}
        for t, token in enumerate(sentence.tokens):
            for _t, _token in enumerate(sentence.tokens):
                if _token.to_str() == token.head_token.to_str():
                    mapa_dephead[t] = _t
                    break
        for t, token in enumerate(sentence.tokens):      
            if t and (sentence.tokens[t-1].id == token.id or (not '-' in token.id and not '-' in sentence.tokens[t-1].id and int(sentence.tokens[t-1].id) > int(token.id))):
                token.id = str(int(sentence.tokens[t-1].id)+1)
        for t, token in enumerate(sentence.tokens):
            token.dephead = sentence.tokens[mapa_dephead[t]].id if t in mapa_dephead else "0"


    print(corpus.to_str())
    
    with open("lista_faltantes.log", 'w') as f:
        f.write("\n\n".join(lista_faltantes))

    with open("dep_lugar_errado.log", "w") as f:
        f.write("\n".join(dep_lugar_errado))

elif corpus.startswith("#"):
    
    try:
        corpus = estrutura_ud.Corpus(recursivo=True, encoding="utf-8")
        corpus.load(sys.argv[1])
    except:
        corpus = estrutura_ud.Corpus(recursivo=True, encoding="latin-1")
        corpus.load(sys.argv[1])

    acdc = []
    for sentence in corpus.sentences.values():
        for i, tag in enumerate(sentence.metadados['xml_tags'].split("|")):
            if tag not in ["</u>", "</t>", "</s>"] and ((acdc and tag != acdc[-1]) or not acdc):
                if tag not in [x.split("=", 1)[1] for token in sentence.tokens for x in token.misc.split("|") if '=' in x]:
                    acdc.append(tag)
            else:
                before_tag = i
                break
                
        contraction = False
        num_contraction = 0
        max_contraction = 1
        MWE_anterior = ""
        save_tag_after = ""
        save_tag_b4 = ""

        for token in sentence.tokens:

            if contraction:        
                if num_contraction > max_contraction:
                    if save_tag_b4:
                        if save_tag_b4 != acdc[-1]:
                            acdc.append(save_tag_b4)
                        save_tag_b4 = ""
                    acdc.append("\t".join([tokendict[x] for x in sorted(tokendict) if tokendict[x]]))
                    if save_tag_after:
                        if save_tag_after != acdc[-1]:
                            acdc.append(save_tag_after)
                        save_tag_after = ""
                    contraction = False
                    num_contraction = 0
                    max_contraction = 1
                else:
                    if "TAGB4=" in token.misc:
                        save_tag_b4 = token.misc.split("TAGB4=")[1].split("|")[0]
                    if "TAGAFTER=" in token.misc:
                        save_tag_after = token.misc.split("TAGAFTER=")[1].split("|")[0]
                    tokendict[1] = sentence.metadados['obra'].split(" ")[0]
                    tokendict[2] = sentence.metadados['obra'].split(" ")[1]
                    tokendict[4] = sentence.metadados['obra'].split(" ")[3]
                    tokendict[6] = sentence.metadados['obra'].split(" ")[-1]
                    tokendict[8] += '+' + token.lemma if tokendict[8] else token.lemma
                    tokendict[9] += '+' + token.upos if tokendict[9] else token.upos
                    tokendict[10] = token.feats.split("|")[0]
                    try:
                        tokendict[11] = token.feats.split("|")[1]
                    except:
                        raise Exception(token.to_str())
                    tokendict[12] = token.feats.split("|")[2]
                    tokendict[13] += '+' + token.deprel if tokendict[13] else token.deprel
                    tokendict[15] = token.deps
                    tokendict[17] += '+' + token.id + '->' + token.dephead if tokendict[17] else token.id + '->' + token.dephead
                    tokendict[18] += '+' + token.xpos if tokendict[18] else token.xpos
                
                    for misc in token.misc.split("|"):
                        try:
                            tokendict[int(misc.split('=')[0])] = misc.split('=')[1]
                        except:
                            continue
                    num_contraction += 1
                    continue

            if not '-' in token.id and not contraction:         
                tokendict = {}
                tokendict[0] = token.word if token.word else "--"
                tokendict[1] = sentence.metadados['obra'].split(" ")[0]
                tokendict[2] = sentence.metadados['obra'].split(" ")[1]
                tokendict[4] = sentence.metadados['obra'].split(" ")[3]
                tokendict[6] = sentence.metadados['obra'].split(" ")[-1]
                tokendict[8] = token.lemma
                tokendict[9] = token.upos
                tokendict[10] = token.feats.split("|")[0]
                try:
                    tokendict[11] = token.feats.split("|")[1]
                except:
                    raise Exception(token.to_str())
                tokendict[12] = token.feats.split("|")[2]
                tokendict[13] = token.deprel
                tokendict[15] = token.deps
                tokendict[17] = token.id + '->' + token.dephead
                tokendict[18] = token.xpos
                
                for misc in token.misc.split("|"):
                    try:
                        tokendict[int(misc.split('=')[0])] = misc.split('=')[1]
                    except:
                        continue
                
                if "TAGB4=" in token.misc and ((acdc and token.misc.split("TAGB4=")[1].split("|")[0] != acdc[-1]) or not acdc):
                    acdc.append(token.misc.split("TAGB4=")[1].split("|")[0])
                acdc.append("\t".join([tokendict[x] for x in sorted(tokendict)]))
                if "TAGAFTER=" in token.misc and ((acdc and token.misc.split("TAGAFTER=")[1].split("|")[0] != acdc[-1]) or not acdc):
                    acdc.append(token.misc.split("TAGAFTER=")[1].split("|")[0])
                continue

            elif '-' in token.id:
                contraction = True
                max_contraction = int(token.id.split("-")[1]) - int(token.id.split("-")[0])
                num_contraction = 0
                tokendict = {i: '' for i in range(30)}
                tokendict[0] = token.word if token.word else "--"
                continue

        for i, tag in enumerate(sentence.metadados['xml_tags'].split("|")):
            if i >= before_tag and tag != acdc[-1]:
                acdc.append(tag)

    print("\n".join(acdc))