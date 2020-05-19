from Test.test_model import *
import re,pandas as pd,numpy as np

df2=pd.read_csv('data/chatbot.csv')
df2=df2.iloc[:,1:]
col_dict={'vendor':'org_name','sitegroup': 'GROUP_NAME','sitenm': 'Site_Name','sitenb': 'Site_nbr', 'account':'ACCT_NBR',
       'utility':'UTILITY_TYPE_NAME','location': 'STAT_ABRV','year': 'BLNG_YEAR','month': 'BLNG_MONTH','spend':'SPEND', 'usage':'IMAGE_USAGE' }

months_df = pd.DataFrame({'abbr': ['jan', 'feb', 'mar', 'apr', 'may', 'jun','jul', 'aug', 'sep', 'oct', 'nov', 'dec'],'full': ['january', 'february', 'march', 'april', 'may', 'june', 'july','august', 'september', 'october', 'november', 'december'],'entr_num':['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']})


tests=['which is the max spend  in  may  for  2017  for  alaska','which is the highest spending site','which is the max spend  in  may  for  2017  for  sitegroup alaska']

testing_statement=tests[2]
l=testing_statement.split()
model_test_statement=[]

for i in l:
    stemed_word = nltk.PorterStemmer().stem(i)
    lemmetized_word = nltk.WordNetLemmatizer().lemmatize(i)
    if i in vocab.keys():
        model_test_statement.append(vocab[i])
    elif stemed_word in vocab.keys():
        model_test_statement.append(vocab[stemed_word])
    elif lemmetized_word in vocab.keys():
        model_test_statement.append(vocab[lemmetized_word])
    else:
        model_test_statement.append(208)

if len(model_test_statement)<25:
    for i in range(len(model_test_statement),25):
        model_test_statement.append(208)

st=torch.tensor(model_test_statement,dtype=torch.long)
f= model(st)

sent_input=testing_statement.split()
tags_pred=[indx2tag[i] for i in f.max(dim=1).indices.tolist()[:len(sent_input)] ]  # if (indx2tag[i] != 'PAD')]


pred_word_tag={tags_pred[i]:word for i,word in enumerate(sent_input)}

aggr_func=False
by=False
utility1=False
master_list=[]
master_list_var=[]

for i in tags_pred:
    if not aggr_func:
        if i=='max': aggr_func=np.max ;x=1
        elif i=='min': aggr_func=np.max ;x=1
        elif i=='sum' : aggr_func=np.sum ;x=1
        elif i == 'count': aggr_func = np.count_nonzero  ;x=1
        elif i=='mean':aggr_func=np.mean ;x=1
        elif i=='var':aggr_func=np.var ;x=1

    if not by:
        if i=='spend': by='spend'
        elif i=='usage' : by ='usage'
        elif i=='usage_electric' : by= 'usage'; utility1='electric'
        elif  i=='usage_water' : by= 'usage'; utility1='water'
        elif i == 'usage_gas': by = 'usage';    utility1 = 'gas'
        elif i == 'demand':     by = 'usage';    utility1 = 'electric'

    if i.endswith('0') and i not in master_list:
        master_list.append(i)
    elif i.endswith('1') and i not in master_list_var:
        master_list_var.append(i)
        master_list.append(re.sub('1','0',i))


for i in months_df.columns:
    x=(months_df[i]==pred_word_tag['month1']).tolist()
    if True in x:
        pred_word_tag['month1']=(x.index(True)+1)
        break

if utility1:
    master_list.append('utility')
    pred_word_tag['utility']=utility1
    master_list_var.append('utility')
if by:
    master_list.append(by)

final_cols=[col_dict[''.join(re.findall('[a-zA-Z]',i))] for i in master_list]


sub_query_dict={}
for i in master_list_var:
    sub_query_dict[col_dict[''.join(re.findall('[a-zA-Z]',i))]]= pred_word_tag[i]


df1=df.loc[(df[list(sub_query_dict)]==pd.Series(sub_query_dict)).all(axis=1)]

pd.DataFrame.groupby(by=master_list)

df1.groupby(by=master_list,level=['SPEND','IMAGE_USAGE'],)

