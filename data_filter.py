from Test.test_model import *
import re,pandas as pd,numpy as np

df2=pd.read_csv('data/chatbot.csv')
df2=df2.iloc[:,1:]

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
utility=False

for i in tags_pred:
    if not aggr_func:
        if i=='max': aggr_func=np.max()
        elif i=='min': aggr_func=np.max()
        elif i=='sum' : aggr_func=np.sum()
        elif i == 'count': aggr_func = np.count_nonzero()
        elif i=='mean':aggr_func=np.mean()
        elif i=='var':aggr_func=np.var()

    if not by:
        if i=='spend': by='spend'
        elif i=='usage' : by ='usage'
        elif i=='usage_electric' : by= 'usage'; utility='electric'
        elif  i=='usage_water' : by= 'usage'; utility='water'
        elif i == 'usage_gas': by = 'usage';    utility = 'gas'



