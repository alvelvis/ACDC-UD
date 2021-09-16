import pandas as pd
from conll_df import conll_df

                                
class Restrictions:
    
    def __init__(self, type_filter):
        self.type_filter = type_filter
        
    def calculate_restrictions(self, df):
        all_X = set(df['x'])
        all_PronType = set(df['type'])
        print('all_X: {}\n\nall_PronType:{}'.format(all_X,all_PronType))
        
        ## Filters
        self.setA=set(['ADP','CCONJ','SCONJ','DET','PRON'])
        self.setB=all_X - self.setA - set(['PUNCT'])
        self.SetPronTypeA = set(['Rel', 'Int'])
        self.SetPronTypeB = all_PronType - self.SetPronTypeA
        print('setA:', self.setA)
        print('setB:', self.setB)
        print('SetPronTypeA:', self.SetPronTypeA)
        print('SetPronTypeB:', self.SetPronTypeB)
    
    def pass_rules_gramaticais(self, row_1,row_2):
        gram_a = row_1.x
        gram_b = row_2.x
        PronType_a = row_1.type
        PronType_b = row_2.type
        if (gram_a in self.setA) or (gram_b in self.setA) or \
           (PronType_a in self.SetPronTypeA) or (PronType_b in self.SetPronTypeA):
            return True
        #print(gram_a, gram_b, PronType_a, PronType_b)
        return False

    def pass_rules_lexicais(self, row_1,row_2):
        gram_a = row_1.x
        gram_b = row_2.x
        PronType_a = row_1.type
        PronType_b = row_2.type
        if ((gram_a in self.setB) and (PronType_a in self.SetPronTypeB)) and \
           ((gram_b in self.setB) and (PronType_b in self.SetPronTypeB)) and \
           ((row_1.Voice and row_2.Voice and row_1.Voice == row_2.Voice) or (not row_1.Voice and not row_2.Voice)) and \
           ((not row_1.VerbForm and not row_2.VerbForm) or (row_1.VerbForm and row_2.VerbForm and row_1.VerbForm == "Part" and row_2.VerbForm == "Part") or (row_1.VerbForm and row_2.VerbForm and row_1.VerbForm != "Part" and row_2.VerbForm != "Part")):
            return True
        #print(gram_a, gram_b, PronType_a, PronType_b)
        return False

    def is_duplicated(self, pair_pair_ngram):
        return pair_pair_ngram[0] == pair_pair_ngram[1]

    def get_pair_ngram(self, sent_df, row):
        none_result = ("","",False,"","","","")
        try:
            i = row.name
            j = row.g
            #print("i,j: ",i,j)
            if int(i)<int(j):
                row_1 = row
                row_2 = sent_df.loc[j]
                pair_pair_ngram = (row_1['prev_pair_ngram'], row_2['next_pair_ngram'], False, \
                                   row_1.type, row_2.type, \
                                   row_1.x, row_2.x)
            else:
                row_1 = sent_df.loc[j]
                row_2 = row
                pair_pair_ngram = (row_1['prev_pair_ngram'], row_2['next_pair_ngram'], True, \
                                   row_1.type, row_2.type, \
                                   row_1.x, row_2.x)                
                        
            if self.is_duplicated(pair_pair_ngram):
                #print('is duplicated', pair_pair_ngram)
                return none_result
            
            if self.type_filter=='gramaticais':
                if self.pass_rules_gramaticais(row_1,row_2):
                    return pair_pair_ngram
                else:
                    #print('not pass rules gramaticais')  
                    return none_result
            
            elif self.type_filter=='lexicais':
                if self.pass_rules_lexicais(row_1,row_2):
                    return pair_pair_ngram
                else:
                    #print('not pass rules lexicais')  
                    return none_result
            else:
                raise Exception('unknown filter type (gramaticais, lexicais): {}'.format(self.type_filter))
                
        except Exception as e:
            #print('error:',e)
            return none_result
            

def preprocessing(file_path):
    df = conll_df(file_path, file_index=False, encoding='utf-8', skip_meta=False)
    #df['l-x'] = df.apply(lambda x:x.l + '-' + x.x , axis=1)
    df['l-x'] = df.apply(lambda x:x.l, axis=1)
    df['g'] = df['g'].astype(str)
    return df
        
def process_result(args):
    df, type_filter, restrictions, i = args
    sent_df = df.loc[i]   
    #sent_df = pd.concat([pd.DataFrame([{'l-x': '<start>'}]), \
    #                                    sent_df, \
    #                     pd.DataFrame([{'l-x': '<end>'}])], ignore_index=True)
    sent_df = pd.concat([pd.DataFrame([{'l-x': '<start>'}], index=['0']), \
                                    sent_df, \
                     pd.DataFrame([{'l-x': '<end>'}], index=['-1'])])

    sent_df['prev_ngram']=sent_df['l-x'].shift(periods=1)
    sent_df['prev_x']=sent_df['x'].shift(periods=1)
    sent_df['prev_type']=sent_df['type'].shift(periods=1)
    if type_filter=='gramaticais':
        sent_df['prev_pair_ngram'] = sent_df.apply(lambda row:(row['prev_ngram'], row['l-x']), axis=1)
    elif type_filter=='lexicais':
        sent_df['prev_pair_ngram'] = sent_df.apply(lambda row:row['l-x'], axis=1)
    else:
        raise Exception('unknown filter type (gramaticais, lexicais): {}'.format(type_filter))
    
    
    sent_df['next_ngram']=sent_df['l-x'].shift(periods=-1)
    sent_df['next_x']=sent_df['x'].shift(periods=-1)
    sent_df['next_type']=sent_df['type'].shift(periods=-1)
    
    if type_filter=='gramaticais':
        sent_df['next_pair_ngram'] = sent_df.apply(lambda row:(row['l-x'], row['next_ngram']), axis=1)
    elif type_filter=='lexicais':
        sent_df['next_pair_ngram'] = sent_df.apply(lambda row:row['l-x'], axis=1)
    else:
        raise Exception('unknown filter type (gramaticais, lexicais): {}'.format(type_filter))

    #sent_df.index = ['0'] + list(df.loc[i].index.astype(str)) + ['0']
    sent_df = sent_df.iloc[1:-1]
    sent_df['pair_pair_ngram'] = sent_df.apply(lambda x: restrictions.get_pair_ngram(sent_df,x), axis=1)
    sent_df['pair_ngram_a']=sent_df['pair_pair_ngram'].apply(lambda x:x[0])
    sent_df['pair_ngram_b']=sent_df['pair_pair_ngram'].apply(lambda x:x[1])
    sent_df['reverse']=sent_df['pair_pair_ngram'].apply(lambda x:x[2])
    sent_df['type_a']=sent_df['pair_pair_ngram'].apply(lambda x:x[3])
    sent_df['type_b']=sent_df['pair_pair_ngram'].apply(lambda x:x[4])
    sent_df['x_a']=sent_df['pair_pair_ngram'].apply(lambda x:x[5])
    sent_df['x_b']=sent_df['pair_pair_ngram'].apply(lambda x:x[6])
    sent_df['ii'] = sent_df.index
    sent_df['sent_id_int'] = i
    sent_df = sent_df.dropna(subset=['g'])
    sent_df = sent_df[sent_df.g!="0"]
    
    return sent_df[['ii', 'g', 'pair_ngram_a', 'pair_ngram_b', 'f', 'sent_id_int', \
                            'reverse', 'type_a', 'type_b', 'x_a', 'x_b', 'x', 'sent_id']]
