import nltk,numpy as np,pandas as pd, re,os,random
import torch


questions=['what','which','when','how','list of','provide'] #'tell me','show'

assist_verbs=['is the','are the','has']
main_grups=['site group',	'site',	'account',	'utility',	'bill','location','month','year']


pronouns=['having','has','for','in']
aggr=['highest','most','biggest','largest','smallest','least','maximum','max','min','minimum','average','mean','sum','total','count','greater than','less than','smaller than','higher than','lower than','around','between','from','all','above','below']
by_mains=['cost','spend','usage','consumption','expend','kwh','gallons','kw','demand','peak kw','peak kwh','dth']

utilities=['electric', 'gas', 'sewer', 'trash', 'water']
locations=[s]





def question_template(ques):
    if question[0]=='how':
        assist_verb = random.sample(['much','many'], 1)
        main_grup = random.sample(main_grups, random.randint(1, 3))
        main_grup[0] = main_grup[0] + 's'


    elif question[0]=='provide':
        assist_verb=['the']
        main_grup = random.sample(main_grups, random.randint(1, 3))
    elif question[0]=='list of':
        main_grup = random.sample(main_grups, random.randint(1, 3))
        assist_verb =[ '']




for i in range(10):
    object = ''.join(random.sample(list('absdawqe!13213231#$@%231'), random.randint(1, 20)))

    assist_verb=random.sample(assist_verbs, 1)
    question=random.sample(questions,1)
    main_grup=random.sample(main_grups, random.randint(1, 3))
    utility= random.sample(utilities, random.randint(0, 2))
    pronoun = random.sample(pronouns, 1)
    aggregate = random.sample(aggr, 1)
    by_main = random.sample(by_mains, 1)


    if (re.findall('are',assist_verb[0]).__len__()>0 )and len(main_grup)>0:
        main_grup[0]=main_grup[0]+'s'



    if aggregate[0] in ['average', 'mean', 'around']:
        question[0] = 'what'

    if aggregate[0] in ['greater than','less than','smaller than','higher than','lower than','around','between','from','above','below']:
        temp_value=random.sample(range(0, 9999999), 1)[0]
        if aggregate[0] == 'between':
            aggregate[0] = aggregate[0] +' '+ str(temp_value - random.sample(range(0, temp_value), 1)[0]) + ' and ' + str(
                temp_value)
        elif aggregate[0] == 'from':
            aggregate[0] = aggregate[0] +' '+ str(temp_value-random.sample(range(0,temp_value),1)[0])  +' to '+   str(temp_value)
        else:
            aggregate[0] = aggregate[0] + str(temp_value)


    if by_main[0] in ['kwh','kw','demand','peak kw','peak kwh']:
        utility=random.sample(['electric'],random.randint(0, 1))
        if 'utility' in main_grup:
            main_grup.remove('utility')
    elif by_main in ['dth','decatherm']:
        utility=random.sample(['gas','natural gas'],random.randint(0, 1))
        if 'utility' in main_grup:
            main_grup.remove('utility')
    elif by_main in ['gal','gallons']:
        utility = random.sample(['water', 'sewer','trash'], random.randint(0, 2))
        if 'utility' in main_grup:
            main_grup.remove('utility')


    if utility.__len__()>1:
        utility=['for'] + ' and '.join(utility)






        x =question+assist_verb + main_grup+pronoun+aggregate+by_main+['for'] + ' and '.join(utility)
    else:
        x = question + assist_verb + main_grup + pronoun +aggregate+ by_main
    if assist_verb[0]=='much':
        x= question+assist_verb+by_main+ random.sample(['happened','occured',])+['for']+main_grup
    print(' '.join(x))


