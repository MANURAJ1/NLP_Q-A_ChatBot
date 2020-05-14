import nltk,numpy as np,pandas as pd, re,os,random
# import torch

sentences=[]
sent_labels=[]

questions=['what','which','when','how','list of','provide'] #'tell me','show'

assist_verbs=['is the','are the','has']

main_grups=['site group',	'site',	'account',	'utility',	'bill','location','month','year']
main_grups_labels=['sitegroup0',	'site0',	'account0',	'utility0',	'bill0','location0','month0','year0']

pronouns=['having','has','for','in']

aggr1=['highest','most','biggest','largest','smallest','least','maximum','max','min','minimum','average','mean','sum','total','count','lowest']
aggr2=['greater than','less than','smaller than','higher than','lower than','around','between','from','all','above','below']

by_mains=['cost','spend','usage','consumption','expend','kwh','gallons','kw','demand','peak kw','peak kwh','dth']

utilities=['electric', 'gas', 'sewer', 'trash', 'water']
# utilites_labels=['electric0', 'gas0', 'sewer0', 'trash0', 'water0']


locations=['alabama', ' al', 'alaska', ' ak', 'arizona', ' az', 'arkansas', ' ar', 'california', ' ca', 'colorado', ' co', 'connecticut', ' ct', 'delaware', ' de', 'florida', ' fl', 'georgia', ' ga', 'hawaii', ' hi', 'idaho', ' id', 'illinois', ' il', 'indiana', 'iowa', ' ia', 'kansas', ' ks', 'kentucky', 'ky', 'louisiana', ' la', 'maine', ' me', 'maryland', ' md', 'massachusetts', ' ma', 'michigan', ' mi', 'minnesota', ' mn', 'mississippi', ' ms', 'missouri', 'mo', 'montana', ' mt', 'nebraska', ' ne', 'nevada', ' nv', 'new hampshire', ' nh', 'new jersey', ' nj', 'new mexico', ' nm', 'new york', ' ny', 'north carolina', 'nc', 'north dakota', ' nd', 'ohio', ' oh', 'oklahoma', ' ok', 'oregon', ' or', 'pennsylvania', ' pa', 'rhode island', ' ri', 'south carolina', ' sc', 'south dakota', 'sd', 'tennessee', ' tn', 'texas', ' tx', 'utah', ' ut', 'vermont', ' vt', 'virginia', ' va', 'washington', ' wa', 'west virginia', ' wv', 'wisconsin', 'wi', 'wyoming', ' wy']

months=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

years=['2017','2018','2019','2020']

#function for adding individual accoount,site ,sitegroup  to main groups
def main_grup_with_ob(main_grup,ob):
    if main_grup.__contains__('site group'):
        main_grup[main_grup.index('site group')]='site group '+ob
    elif main_grup.__contains__('site'):
        main_grup[main_grup.index('site')]='site '+ob
    elif main_grup.__contains__('account'):
        main_grup[main_grup.index('account')]='account '+ob
    return main_grup


def label_generator(item,property):
    item=''.join(item).split()
    item = ['O' for i in item]
    item[len(item) - 1] =  property
    return item

def question_template(ques,object):

    utility_label=[]
    location_label=[]
    month_label=[]
    year_label=[]
    by_main_label=[]
    main_grup_label=[]

    random_selection=random.sample([0,1],1)[0]
    temp_num_check=0

    if ques=='what':
        assist_verb = random.sample(['is the', 'are the'], 1)
        aggregate = random.sample(aggr1, random.randint(0,1))
        by_main= random.sample(by_mains, 1)
        main_grup = random.sample(main_grups, random.randint(0, 3))
        month = random.sample(months, random.randint(0, 1))
        location = random.sample(locations, random.randint(0, 1))
        year= random.sample(years, random.randint(0, 1))
        utility = random.sample(utilities, random.randint(0, 1))

        if (re.findall('are', assist_verb[0]).__len__() > 0) and len(main_grup) > 0:
            main_grup[0] = main_grup[0] + 's'

        if random_selection:
            ob=object
            main_grup=main_grup_with_ob(main_grup,ob)

        year_and_mnth=False

        if main_grup.count('month')>0:
            main_grup.remove('month')
            if main_grup.count('year')>0:
                year_and_mnth=True
            if month.__len__()>0:
                month=random.sample([' for the month  ',' in the month '], 1)+random.sample(['', ' of '], 1) +month
                month_label=label_generator(month,'month1')
            else:
                month=random.sample([' for all months',' months ','monthwise'], 1)
                month_label = label_generator(month, 'month0')
        elif month.__len__()>0:
            month = random.sample([' for ', ' in '], 1) + month
            month_label = label_generator(month, 'month1')


        if main_grup.count('year') > 0:
            main_grup.remove('year')
            if year_and_mnth:
                year_txt='and year'
                if year.__len__() > 0:
                    year=['and year '+ year]
                    year_label= label_generator(year,'year1')
                else:
                    year = random.sample([' for year', ' in year ' ,'yearwise'], 1) + random.sample(['', ' of '], 1) + month
                    year_label=label_generator(year,'month1')
        elif year.__len__() > 0:
            year = random.sample([' for ', 'in '], 1)+year
            year_label=label_generator(year, 'year1')


        if main_grup.count('location'):
            main_grup.remove('location')
            if len(location)>0:
                location=random.sample([' for ',' in '],1) + random.sample(['location','state','area'],1)+ location
                location_label=label_generator(location,'location1')
            else:
                location=random.sample([' for all ',' in all ',' by ' ],1) + random.sample(['locations','states','areas'],1)
                location_label=label_generator(location,'location0')
        elif len(location)>0:
            location = random.sample([' for ', 'in '], 1) + location
            location_label=label_generator(location,'location1')


        if by_main[0] in ['kwh','kw','demand','peak kw','peak kwh']:
            utility=random.sample(['electric'],random.randint(0, 1))
            util='electric'
            temp_num_check=1
        elif by_main[0] in ['dth','decatherm']:
            utility=random.sample(['gas','natural gas'],random.randint(0, 1))
            temp_num_check = 1
        elif by_main[0] in ['gal','gallons']:
            utility = random.sample(['water', 'sewer','trash'], random.randint(0, 2))
            temp_num_check = 1

        # if temp_num_check and len(utility)==0:
        by_main_label=label_generator(by_main,by_main[0])

        if main_grup.count('utility'):
            main_grup.remove('utility')
            if len(utility) > 0:
                utility = random.sample([' for ', ' by '], 1) + utility
                utility_label = label_generator(utility, 'utility1')
            elif temp_num_check == 1:
                utility =[]
            else:
                utility = random.sample([' for all utilities ', ' by all utilities '], 1)
                utility_label = label_generator(utility, 'utility0')
        elif len(utility) > 0:
            utility = random.sample([' for ', 'by '], 1) + utility
            utility_label = label_generator(utility, 'utility1')



        if len(main_grup) > 0:
            if len(main_grup[0].split()) > 1:
                main_grup_label=[main_grup[0].split()[0]+'0',main_grup[0].split()[0]+'1']
            else:
                main_grup_label = [main_grup[0].split()[0] + '0']
            main_grup[0]=random.sample([' for ', 'of '], 1)[0]+main_grup[0]
            main_grup_label=['O']+main_grup_label
        if len(main_grup)>1 and len(main_grup)<2:
            main_grup= [' and '.join(main_grup)]
            main_grup_label.append('O')
            main_grup_label.append(main_grup[1]+'0')
        elif len(main_grup)>2:
            main_grup_label.append('O')
            main_grup_label.append(main_grup[2] + '0')


        sentence=[ques]+assist_verb+aggregate+by_main+main_grup+utility+month+year+location
        sent_label=['O','O','O']+['aggr0']+by_main_label+main_grup_label+utility_label+month_label+year_label+location_label

        sentences.append(sentence)
        sent_labels.append(sent_label)

        print(len(' '.join(sentence).split()),len(sent_label))
        print(sent_label)
        return print(' '.join(sentence))

    # elif question[0]=='how':
    #     assist_verb = random.sample(['much','many'], 1)
    #     main_grup = random.sample(main_grups, random.randint(1, 3))
    #     main_grup[0] = main_grup[0] + 's'
    #
    #
    #
    # elif question[0]=='provide':
    #     assist_verb=['the']
    #     main_grup = random.sample(main_grups, random.randint(1, 3))
    # elif question[0]=='list of':
    #     main_grup = random.sample(main_grups, random.randint(1, 3))
    #     assist_verb =[ '']




for i in range(10):


    #
    object = ''.join(random.sample(list('absdawqe!13213231#$@%231'), random.randint(1, 20)))
    question_template('what', object)
    #
    # assist_verb=random.sample(assist_verbs, 1)
    # question=random.sample(questions,1)
    # main_grup=random.sample(main_grups, random.randint(1, 3))
    # utility= random.sample(utilities, random.randint(0, 2))
    # pronoun = random.sample(pronouns, 1)
    # aggregate = random.sample(aggr, 1)
    # by_main = random.sample(by_mains, 1)
    #
    #
    #
    #
    #
    #
    #
    # if aggregate[0] in ['greater than','less than','smaller than','higher than','lower than','around','between','from','above','below']:
    #     temp_value=random.sample(range(0, 9999999), 1)[0]
    #     if aggregate[0] == 'between':
    #         aggregate[0] = aggregate[0] +' '+ str(temp_value - random.sample(range(0, temp_value), 1)[0]) + ' and ' + str(
    #             temp_value)
    #     elif aggregate[0] == 'from':
    #         aggregate[0] = aggregate[0] +' '+ str(temp_value-random.sample(range(0,temp_value),1)[0])  +' to '+   str(temp_value)
    #     else:
    #         aggregate[0] = aggregate[0] + str(temp_value)
    #
    #
    #
    #
    # if utility.__len__()>1:
    #     utility=['for'] + ' and '.join(utility)
    #
    #
    #
    #
    #
    #
    #     x =question+assist_verb + main_grup+pronoun+aggregate+by_main+['for'] + ' and '.join(utility)
    # else:
    #     x = question + assist_verb + main_grup + pronoun +aggregate+ by_main
    # if assist_verb[0]=='much':
    #     x= question+assist_verb+by_main+ random.sample(['happened','occured',])+['for']+main_grup
    # print(' '.join(x))


