from Test.test_model import model,torch,indx2tag,indx2word,vocab,tags
import re,pandas as pd,numpy as np,nltk

# df=pd.read_csv('data/chatbot.csv')
df=pd.read_csv('data/chatbot.csv')
df=df.iloc[:,1:]
col_dict={'vendor':'org_name','sitegroup': 'GROUP_NAME','sitenm': 'Site_Name','sitenb': 'Site_nbr', 'account':'ACCT_NBR','bill':'BILL_IDFR',
       'utility':'UTILITY_TYPE_NAME','location': 'STAT_ABRV','year': 'BLNG_YEAR','month': 'BLNG_MONTH','spend':'SPEND', 'usage':'IMAGE_USAGE' }

months_df = pd.DataFrame({'abbr': ['jan', 'feb', 'mar', 'apr', 'may', 'jun','jul', 'aug', 'sep', 'oct', 'nov', 'dec'],'full': ['january', 'february', 'march', 'april', 'may', 'june', 'july','august', 'september', 'october', 'november', 'december'],'entr_num':['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']})



location_df=pd.DataFrame({'full':['Alabama'	,'Alaska'	,'Arizona'	,'Arkansas'	,'California'	,'Colorado'	,'Connecticut'	,'Delaware'	,'Florida'	,'Georgia'	,'Hawaii'	,'Idaho'	,'Illinois'	,'Indiana'	,'Iowa'	,'Kansas'	,'Kentucky'	,'Louisiana'	,'Maine'	,'Maryland'	,'Massachusetts'	,'Michigan'	,'Minnesota'	,'Mississippi'	,'Missouri'	,'Montana'	,'Nebraska'	,'Nevada'	,'New Hampshire'	,'New Jersey'	,'New Mexico'	,'New York'	,'North Carolina'	,'North Dakota'	,'Ohio'	,'Oklahoma'	,'Oregon'	,'Pennsylvania'	,'Rhode Island'	,'South Carolina'	,'South Dakota'	,'Tennessee'	,'Texas'	,'Utah'	,'Vermont'	,'Virginia'	,'Washington'	,'West Virginia'	,'Wisconsin'	,'Wyoming'],'abbr':[' AL'	,'AK'	,'AZ'	,'AR'	,'CA'	,'CO'	,'CT'	,'DE'	,'FL'	,'GA'	,'HI'	,'ID'	,'IL'	,'IN'	,'IA'	,'KS'	,'KY'	,'LA'	,'ME'	,'MD'	,'MA'	,'MI'	,'MN'	,'MS'	,'MO'	,'MT'	,'NE'	,'NV'	,'NH'	,'NJ'	,'NM'	,'NY'	,'NC'	,'ND'	,'OH'	,'OK'	,'OR'	,'PA'	,'RI'	,'SC'	,'SD'	,'TN'	,'TX'	,'UT'	,'VT'	,'VA'	,'WA'	,'WV'	,'WI'	,'WY'	]})
location_df.full=location_df.full.apply(str.lower)
location_df.abbr=location_df.abbr.apply(str.lower)


def main_func( testing_statement):
    testing_statement = re.sub('site *group', 'sitegroup', testing_statement)
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

    for i,w in enumerate(tags_pred):
        if w in ['site_group0','site_group00']:
            tags_pred[i]='sitegroup0'
        elif w =='site_group1':
            tags_pred[i] = 'sitegroup1'

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
            elif i == 'count': aggr_func = len  ;x=1
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
            if re.sub('1', '0', i) not in master_list:
                master_list.append(re.sub('1','0',i))

    if 'month1' in pred_word_tag:
        for i in months_df.columns:
            month_nbr=(months_df[i]==pred_word_tag['month1']).tolist()
            if True in month_nbr:
                pred_word_tag['month1']=(month_nbr.index(True)+1)
                break

    if 'location1' in pred_word_tag:
        for i in location_df.columns:
            location_state=(location_df[i]==pred_word_tag['location1']).tolist()
            if True in location_state:
                pred_word_tag['location1']=location_df.abbr[location_state.index(True)]
                pred_word_tag['location1']=str.upper(pred_word_tag['location1'])
                break

    if 'year1' in pred_word_tag:
        pred_word_tag['year1']=int(pred_word_tag['year1'])


    if ('site0' ) in master_list:
        master_list.remove('site0')
        master_list.append('sitenm')
        master_list.append('sitenb')

    if 'site1' in master_list_var:
        if pred_word_tag['site1'] in df.Site_nbr.to_list():
            master_list_var.remove('site1')
            master_list_var.append('sitenb')
            pred_word_tag['sitenb']=pred_word_tag['site1']
        elif pred_word_tag['site1'] in df.Site_Name.to_list():
            master_list_var.remove('site1')
            master_list_var.append('sitenm')
            pred_word_tag['sitenm'] = pred_word_tag['site1']


    if utility1:
        master_list.append('utility')
        pred_word_tag['utility']=utility1
        master_list_var.append('utility')
    if by:
        master_list.append(by)

    print(pred_word_tag,master_list_var,master_list)

    final_cols=[col_dict[''.join(re.findall('[a-zA-Z]',i))] for i in master_list]

    sub_query_dict={}
    for i in master_list_var:
        if i in ['month1','year1']:
            sub_query_dict[col_dict[''.join(re.findall('[a-zA-Z]', i))]] = pred_word_tag[i]
        else:
            sub_query_dict[col_dict[''.join(re.findall('[a-zA-Z]',i))]]= str.upper(pred_word_tag[i])


    print(sub_query_dict,final_cols,by)

    df1=df.loc[(df[list(sub_query_dict)]==pd.Series(sub_query_dict)).all(axis=1)]

    df1=df1[final_cols]
    if aggr_func!=len and by:
        if final_cols.__len__()==1 and final_cols[0]==col_dict[''.join(re.findall('[a-zA-Z]', by))]:
            df2=df1
        else:
            df2=df1.groupby(final_cols[:-1]).sum().reset_index()
    else:
        df2=df1

    if df2.shape[0]==0:
        print('No data found')
    else:
        if aggr_func:
            if aggr_func == len:
                print(aggr_func(df2))
                print(df2[final_cols].head())
            else:
                print(aggr_func(df2[col_dict[by]]))
                print(df2[final_cols].head())
        else:
            print(df2[final_cols].head())

    return 1




tests=['which is the max spend  in  may  for  2017  for  alaska','which is the highest spending site','which is the max spend  in  may  for  2017  for  sitegroup in wyoming','what is count of accounts for site 410-01-410000-1117  and sitegroup signal   in ks','count of bills in 2020']


testing_statement=tests[4]
# testing_statement='start'
while testing_statement!='quit':
    testing_statement=input('please enter')
    main_func(testing_statement)

GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{<GOOGLE_CLOUD_SPEECH_CREDENTIALS from text file>
 }"""

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone(2) as source:
    print("Say something!")
    audio = r.listen(source)

try:
    testing_statement=r.recognize_google_cloud(audio,
                             credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    print("Google Cloud Speech thinks you said " +testing_statement )
    main_func(testing_statement)
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))
