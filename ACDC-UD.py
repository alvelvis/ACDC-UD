import sys
import re
import estrutura_ud
import pprint

arquivo = sys.argv[1]

def from_ACDC_to_UD(arquivo):
    with open(arquivo, encoding="latin-1") as f:
        ACDC = f.read()
        
    if "<obra id=" in ACDC:
        lista_tags = []
        sentences = []
        tokens = []
        lista_faltantes = []
        i = 0
        MWE = False
        for l, linha in enumerate(ACDC.splitlines()):
            #print(linha)
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
                if '+' in linha.split("\t")[17]:
                    tokens.append(linha.split("\t")[17].split("->")[0] + "-" + linha.split("\t")[17].split("+")[-1].split("->")[0] + "\t" + linha.split("\t")[0] + "\t" + "\t".join("________"))
                for i in range(len(linha.split("\t")[17].split("+")) -1):
                    if not linha.split("\t")[17].split("+")[i]:
                        lista_faltantes.append(ACDC.splitlines()[l-1] + "\n" + ACDC.splitlines()[l])
                        continue
                    word = linha.split("\t")[0]
                    misc_21 = linha.split("\t")[21] if len(linha.split("\t")) > 20 else ""
                    misc_20 = linha.split("\t")[20] if len(linha.split("\t")) > 19 else ""
                    misc_19 = linha.split("\t")[19] if len(linha.split("\t")) > 18 else ""
                    misc = [linha.split("\t")[14], linha.split("\t")[16], linha.split("\t")[18], misc_19, misc_20, misc_21]
                    tokens.append("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                            linha.split("\t")[17].split("+")[i].split("->")[0] if '+' in linha.split("\t")[17] else linha.split("\t")[17].split("->")[0],
                            word,
                            linha.split("\t")[8].split("+")[i],
                            linha.split("\t")[9],
                            "_",
                            "|".join([linha.split("\t")[10], linha.split("\t")[11], linha.split("\t")[12]]),
                            linha.split("\t")[17].split("+")[i].split("->")[1] if '+' in linha.split("\t")[17] else linha.split("\t")[17].split("->")[1],
                            linha.split("\t")[13],
                            linha.split("\t")[15],
                            "|".join(misc) if not MWE else "|".join(sorted(misc + ["MWE=" + MWE_lema.replace("=", "_"), "MWEPOS=" + MWE_pos])),
                            ))

            if '</u>' in linha.strip():
                sentence = f"# sent_id = {obra.strip().replace(' ', '-')}-{i}\n"
                sentence += f"# obra = {obra}\n"
                sentence += f"# tituloobra = {tituloobra}\n"
                sentence += f"# autor = {autor}\n"
                sentence += f"# xml_tags = {'|'.join(lista_tags)}\n"
                sentence += f'# text = ' + " ".join([x.split("\t")[1] for x in tokens]) + "\n"
                sentence += "\n".join(tokens)
                sentences.append(sentence)
                lista_tags = []
                tokens = []
                i += 1

        print("\n\n".join(lista_faltantes))                


from_ACDC_to_UD(arquivo)