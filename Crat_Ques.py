import random,pandas as pd,numpy as np,re,os

questions=['what','which','when','how','list of','provide','tell me']

assist_verbs=['is the','are the','has']
main_grups=['site group',	'site',	'acct',	'utility',	'bill','location','month','year']
object=''.join(random.sample(list('absdawqe!13213231#$@%231'),random.randint(1,20)))

pronouns=['having','has','for','in']
aggr=['highest','most','biggest','largest','smallest','least','maximum','max','min','minimum','average','mean','sum','total','count','greater than','less than','smaller than','bigger than','between','around','in between','among']
by_mains=['cost','spend','usage','consumption','expend','kwh','gallons','kw','demand','peak kw','peak kwh','dth']

utilities=['electric', 'gas', 'sewer', 'trash', 'water']



for i in range(10):
    assist_verb=random.sample(assist_verbs, 1)
    question=random.sample(questions,1)
    main_grup=random.sample(main_grups, random.randint(0, 3))
    utility= random.sample(utilities, random.randint(0, 2))
    pronoun = random.sample(pronouns, 1)
    aggregate = random.sample(aggr, 1)
    by_main = random.sample(by_mains, 1)
    if (re.findall('are',assist_verb[0]).__len__()>0 )and len(main_grup)>0:
        main_grup[0]=main_grup[0]+'s'

    if question[0]=='how':
        assist_verb = random.sample(['much','many'], 1)
        main_grup[0] = main_grup[0] + 's'
    elif question[0]=='provide':
        assist_verb=['the']
    elif question[0] in['list of','tell me','provide']:
        assist_verb = ['']





    if utility.__len__()>1:
        x =question+assist_verb + main_grup+pronoun+aggregate+by_main+['for'] +utility
    else:
        x = question + assist_verb + main_grup + pronoun +aggregate+ by_main
    print(' '.join(x))

