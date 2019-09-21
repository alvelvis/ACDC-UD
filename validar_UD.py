import estrutura_ud
import interrogar_UD
import sys
import re
import pprint

def validate(conllu, sent_id = None, errorList = "validar_UD.txt"):
    with open(errorList) as f:
        errorListFile = f.read().splitlines()
        errorList = []
        [errorList.append(x) for x in errorListFile]

    errorDictionary = {}
    for error in errorList:
        comment, parameters = error.split("|", 1)\
            if "|" in error\
                else (error, error)
        comment = comment.strip()
        parameters = parameters.strip()

        for sentString in interrogar_UD.main(conllu, 5, parameters, 0, sent_id)['output']:
            if not comment in errorDictionary:
                errorDictionary[comment] = []
            sentence = estrutura_ud.Sentence(recursivo=True)
            sentence.build(sentString)
            for t, token in enumerate(sentence.tokens):
                if "<b>" in token.to_str():
                    tokenId = re.sub(r"<.*?>", "", re.sub(r"@.*?/", "", token.id))
                    tokenT = t
                    break

            errorDictionary[comment].append({
                "tokenId": tokenId,
                "t": tokenT,
                "sentence": sentence.to_str(),
            })

    return errorDictionary

if __name__ == "__main__":
    pprint.pprint(validate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, sys.argv[3] if len(sys.argv) > 3 else "validar_UD.txt"))