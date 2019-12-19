import sys
import re
import estrutura_ud
import pprint

arquivo = sys.argv[1]

def from_ACDC_to_UD(arquivo):
    with open(arquivo, encoding="latin-1") as f:
        ACDC = f.read()
    if "<obra id=" in ACDC:
        arquivos = [{
            'arquivo': re.findall('<obra id="([^"]+?)"', x)[0].replace(' ', '-'),
            'tituloobra': re.findall('<tituloobra id="([^"]+?)"', x)[0],
            'autor': re.findall('<autor id="([^"]+?)"', x)[0],
            'sentences': [[z for z in y.splitlines() if len(z.split('\t')) > 5] for y in re.findall('<u>(.*?)</u>', x, flags=re.DOTALL) if len(y.split('\t')) > 5],
            } for x in re.findall('<obra id="[^"]+".*?</obra>', ACDC, flags=re.DOTALL)]


        UD = ""
        for arquivo in arquivos:
            sent_id = 0
            for sentence in arquivo['sentences']:
                UD += f"# sent_id = {arquivo['arquivo']}-{sent_id}\n"
                UD += "# tituloobra = " + arquivo['tituloobra'] + "\n"
                UD += "# autor = " + arquivo['autor'] + "\n"
                UD += "# text = " + " ".join([x.split("\t")[0] for x in sentence]) + "\n"

                #transformar em conllu
                sent_ud = ["{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    x.split("\t")[17].split("->", 1)[0], 
                    x.split("\t")[0],
                    x.split("\t")[8],
                    x.split("\t")[9],
                    "_",
                    "|".join([x.split("\t")[10], x.split("\t")[11], x.split("\t")[12]]),
                    x.split("\t")[17].split("->", 1)[1],
                    x.split("\t")[13],
                    "_",
                    "_",
                    ) for x in sentence if len(x.split("\t")) > 15]

                #fazer descontração dos tokens contraídos
                for t, token in enumerate(sent_ud):
                    if '+' in token.split("\t")[6]:
                        #print(token)
                        for i in range(len(token.split("\t")[6].split("+"))):
                            sent_ud[t+1+i:t+1+i] = ["{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                                token.split("\t")[0] if not '->' in token.split("\t")[6].split("+")[i] else token.split("\t")[6].split("+")[i].split("->")[0],
                                token.split("\t")[1], #problema aqui: NA fica com forma NA NA, e não EM A. Os lemas ficam OK
                                token.split("\t")[2].split("+")[i] if '+' in token.split("\t")[2] else token.split("\t")[2],
                                token.split("\t")[3].split("+")[i],
                                "_",
                                token.split("\t")[5],
                                token.split("\t")[6].split("+")[i] if not '->' in token.split("\t")[6].split("+")[i] else token.split("\t")[6].split("+")[i].split("->")[1],
                                token.split("\t")[7].split("+")[i],
                                "_",
                                "_")]

                #criar token head da contração
                for t, token in enumerate(sent_ud):
                    if '+' in token.split("\t")[6]:
                        sent_ud[t] = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                                token.split("\t")[0] + "-" + token.split("\t")[6].split("+")[-1].split("->")[0],
                                token.split("\t")[1],
                                "_",
                                "_",
                                "_",
                                "_",
                                "_",
                                "_",
                                "_",
                                "_")

                UD += "\n".join(sent_ud) + "\n"
                UD += "\n"
                sent_id += 1
        
        print(UD)


from_ACDC_to_UD(arquivo)