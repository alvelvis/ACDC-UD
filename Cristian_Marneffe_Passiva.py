#!/usr/bin/env python
# coding: utf-8

# !python lexicais_gramaticais.py --file_path bosque25_wb.conllu --type_filter gramaticais --ncpus 7

# In[2]:


#get_ipython().system('pip3 install tqdm')


# In[23]:


import pandas as pd
import os
import re
#from nltk.util import ngrams
import pickle
from collections import defaultdict
from tqdm import tqdm
import numpy as np
from multiprocessing import Pool, freeze_support
import argparse
import pickle
from Restrictions_Passiva import Restrictions , process_result, preprocessing
import sys
import json

def main(file_path, type_filter="lexicais", html_file="cristian-marneffe.html"):

    # In[41]:

    ncpus=7


    # In[42]:


    restrictions = Restrictions(type_filter)
    df = preprocessing(file_path)
    restrictions.calculate_restrictions(df)
    sent_total = df.index[-1][0]


    # In[43]:


    df['l_ant_1']=df['l'].shift(periods=1)
    df['l_ant_2']=df['l'].shift(periods=2)


    # In[44]:


    df = df[~(df.l == '_')]


    # In[45]:


    df[~(df.l=='_')].head()


    # In[46]:


    import tqdm


    # In[47]:


    with Pool(ncpus) as p:
        args = [(df, type_filter, restrictions, i) for i in range(1,sent_total+1)]
        results = list(tqdm.tqdm(p.map(process_result, args), total=len(args)))


    # In[48]:


    df_results = pd.concat(results, axis=0)


    # In[49]:


    df_results.head()


    # In[50]:


    #pair_ngram_freq = df_results.groupby(['ii','g','pair_ngram_a','pair_ngram_b','f','sent_id_int','reverse','type_a','type_b',
    #                   'x_a','x_b','x','sent_id'])
    df_results = df_results[~((df_results.pair_ngram_a=='') & (df_results.pair_ngram_b==''))]
    df_results['condition'] = df_results.apply(lambda row:(row.pair_ngram_a,row.pair_ngram_b,row.reverse),axis=1)
    pair_ngram_freq = df_results.groupby('condition')
    #pair_ngram_freq={}
    #for group_name, df_group in groups:
    #    pair_ngram_freq[group_name] = df_group[['reverse','sent_id_int','ii','g', 'type_a','type_b', 'sent_id', 'x_a', 'x_b']]


    # In[51]:


    relevant_pair_ngram_freq ={group_name:df_group for group_name , df_group in  pair_ngram_freq if len(df_group)>1}


    # In[52]:


    len(relevant_pair_ngram_freq)


    # pair_ngram_freq=defaultdict(list)
    # total_results_lines = len(df_results.index)
    # for ind in df_results.index:
    #     group_ngram_distance = df_results.ix[ind]
    #     i, j, ngram_a, ngram_b, relation , sent_id, reverse, type_a, type_b, x_a, x_b, x, sent_id_str = group_ngram_distance
    #     if ngram_a=='' and ngram_b=='':
    #         continue
    #     pair_ngram_freq[(ngram_a, ngram_b, reverse)].append((relation,sent_id,i,j, type_a, type_b, sent_id_str, x_a, x_b))

    # In[53]:


    class color:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'


    # In[54]:


    def get_colored_word(row, word1, word2):
        #if '-' in row.name :
        #    continue
        if row.name == word1:
            bold = '<font color="red"><b>{}</b></font>'.format(row.w)
            return bold #sentence.append(bold)
        elif row.name == word2:
            bold = '<font color="blue"><b>{}</b></font>'.format(row.w)
            return bold #sentence.append(bold)
        else:
            return row.w #sentence.append()


    # In[55]:


    from collections import Counter

    examples = []
    for ind, (group_name, df_group) in enumerate(relevant_pair_ngram_freq.items()):
        if ind%100==0:
            print(ind, end=' ')
        count_relations = Counter(list(df_group.f.values))
        # Caso exista várias relações
        if len(count_relations)>1:
            sentences=[]
            for ind,case_row in df_group.iterrows():
                sent_id = case_row.sent_id_int
                word1 = case_row.ii
                word2 = case_row.g

                sentence = list(df.loc[sent_id].apply(lambda row: get_colored_word(row, word1, word2), axis=1).values)       
                #sentences.append((sentence , rel, sent_id, type_a, type_b, sent_id_str, x_a, x_b))
                sentences.append((sentence , case_row))#rel, sent_id, type_a, type_b, sent_id_str, x_a, x_b))
            examples.append((sentences, group_name, count_relations))


    # In[56]:

    dicionario_marneffe = []

    #reverse if nn[2] else 
    if type_filter=='gramaticais':
        reverse = "<span style='font-size:25px;'>&#8678;</span>"
        no_reverse = "<span style='font-size:25px;'>&#8680;</span>"
        with open(html_file,'w+',encoding="utf-8") as file:

            for i,more_than_sentences in enumerate(examples):

                sentences,nn,a = more_than_sentences
                blue_text = '<font color="blue"><b>{}</b></font>'
                red_text = '<font color="red"><b>{}</b></font>'

                dicionario_marneffe.append({"exemplo": '{} {} <b>-></b> {} {}'.format(
                                                                        nn[0][0], 
                                                                        blue_text.format(nn[0][1]) if nn[2] else  red_text.format(nn[0][1]), 
                                                                        red_text.format(nn[1][0]) if nn[2] else  blue_text.format(nn[1][0]), 
                                                                        nn[1][1]),
                                            "frases": [],
                                            })

                file.write('<p><b>Exemplo {}:</b> ( {} , {} ) <b>{}</b> ( {} , {} )</p>'.format(i+1, 
                                                                        nn[0][0], 
                                                                        blue_text.format(nn[0][1]) if nn[2] else  red_text.format(nn[0][1]), 
                                                                        no_reverse,\
                                                                        red_text.format(nn[1][0]) if nn[2] else  blue_text.format(nn[1][0]), 
                                                                        nn[1][1]))
                counter  = " , ".join(['<b>{}</b> : {}'.format(k,v) for k,v in a.items()])
                file.write('<p>[ {} ]</p>'.format(counter))
                for more_than_sent in sentences:
                    #    'ii','g','pair_ngram_a','pair_ngram_b','f','sent_id_int','reverse','type_a','type_b',
                    #    'x_a','x_b','x','sent_id'
                    sent, case_row = more_than_sent
                    #sent , rel, sent_id, type_a, type_b, sent_id_str, x_a, x_b = more_than_sent
                    sent_id_str  = case_row.sent_id
                    rel = case_row.f
                    type_a = case_row.type_a
                    type_b = case_row.type_b
                    x_a = case_row.x_a
                    x_b = case_row.x_b

                    for i, token in enumerate(sent):
                        if '"red"' in token:
                            id1 = i+1
                            word1 = re.sub(r"<.*?>", "", token)
                        if '"blue"' in token:
                            id2 = i+1
                            word2 = re.sub(r"<.*?>", "", token)
                    dicionario_marneffe[-1]["frases"].append({
                        "id1": id1,
                        "id2": id2,
                        "WORD1": word1,
                        "WORD2": word2,
                        "POS1": x_a,
                        "POS2": x_b,
                        "rel": rel,
                        "sent_id": sent_id_str,
                    })

                    sentence = "<p><b>Frase {}</b> \t: {} - rel: <b>({})</b> ,  type: <b>({} - {})</b> , pos: <b>({} - {})</b> </p>".format(
                        sent_id_str, " ".join(sent), rel,
                        blue_text.format(type_a) if nn[2] else  red_text.format(type_a),
                        red_text.format(type_b) if nn[2] else  blue_text.format(type_b),
                        blue_text.format(x_a) if nn[2] else  red_text.format(x_a),
                        red_text.format(x_b) if nn[2] else  blue_text.format(x_b))

                    file.write('{}\n'.format(sentence))
                file.write('<br>')

        os.remove("cristian-marneffe.html")
        return dicionario_marneffe

    elif type_filter=='lexicais':
        reverse = "<span style='font-size:25px;'>&#8678;</span>"
        no_reverse = "<span style='font-size:25px;'>&#8680;</span>"
        with open(html_file,'w+',encoding="utf-8") as file:
            i=0
            for more_than_sentences in examples:

                pair = more_than_sentences[1][:2]
                #if pair in all_pairs:
                #    continue 
                i+=1    
                sentences,nn,a = more_than_sentences
                blue_text = '<font color="blue"><b>{}</b></font>'
                red_text = '<font color="red"><b>{}</b></font>'

                dicionario_marneffe.append({"exemplo": '{} <b>-></b> {}'.format(
                                                                        blue_text.format(nn[0]) if nn[2] else  blue_text.format(nn[1]), 
                                                                        red_text.format(nn[1]) if nn[2] else  red_text.format(nn[0])
                                                                        ),
                                            "frases": [],
                                            })

                file.write('<p><b>Exemplo {}:</b> {} <b>{}</b>  {}  </p>'.format(i, 
                                                                        blue_text.format(nn[0]) if nn[2] else  red_text.format(nn[0]), 
                                                                        no_reverse,\
                                                                        red_text.format(nn[1]) if nn[2] else  blue_text.format(nn[1])))
                counter  = " , ".join(['<b>{}</b> : {}'.format(k,v) for k,v in a.items()])
                file.write('<p>[ {} ]</p>'.format(counter))
                for more_than_sent in sentences:
                    #    'ii','g','pair_ngram_a','pair_ngram_b','f','sent_id_int','reverse','type_a','type_b',
                    #    'x_a','x_b','x','sent_id'
                    sent, case_row = more_than_sent
                    #sent , rel, sent_id, type_a, type_b, sent_id_str, x_a, x_b = more_than_sent
                    sent_id_str  = case_row.sent_id
                    rel = case_row.f
                    type_a = case_row.type_a
                    type_b = case_row.type_b
                    x_a = case_row.x_a
                    x_b = case_row.x_b

                    for i, token in enumerate(sent):
                        if '"red"' in token:
                            id1 = i+1
                            word1 = re.sub(r"<.*?>", "", token)
                        if '"blue"' in token:
                            id2 = i+1
                            word2 = re.sub(r"<.*?>", "", token)
                    dicionario_marneffe[-1]["frases"].append({
                        "id1": id1,
                        "id2": id2,
                        "WORD1": word1,
                        "WORD2": word2,
                        "POS1": x_a,
                        "POS2": x_b,
                        "rel": rel,
                        "sent_id": sent_id_str,
                    })

                    sentence = "<p><b>Frase {}</b> \t: {} - rel: <b>({})</b> ,  type: <b>({} - {})</b> , pos: <b>({} - {})</b> </p>".format(
                        sent_id_str, " ".join(sent), rel,
                        blue_text.format(type_a) if nn[2] else  red_text.format(type_a),
                        red_text.format(type_b) if nn[2] else  blue_text.format(type_b),
                        blue_text.format(x_a) if nn[2] else  red_text.format(x_a),
                        red_text.format(x_b) if nn[2] else  blue_text.format(x_b))
                    file.write('{}\n'.format(sentence))
                file.write('<br>')

        os.remove("cristian-marneffe.html")
        return dicionario_marneffe
    else:
        raise Exception('unknown filter type (gramaticais, lexicais): {}'.format(type_filter))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




