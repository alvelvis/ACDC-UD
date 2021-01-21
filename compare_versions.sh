set -e
if [ -d "ACDC-UD" ]; then
    folder="ACDC-UD"
    dot="."
else
    folder="."
    dot=".."
fi
meld --diff $folder/interrogar_UD.py $dot/Interrogat-rio/www/cgi-bin/interrogar_UD.py $dot/Julgamento/interrogar_UD.py
meld --diff $folder/estrutura_ud.py $dot/Interrogat-rio/www/cgi-bin/estrutura_ud.py $dot/Julgamento/estrutura_ud.py
meld --diff $folder/validar_UD.txt $dot/Interrogat-rio/www/cgi-bin/validar_UD.txt $dot/Julgamento/validar_UD.txt    