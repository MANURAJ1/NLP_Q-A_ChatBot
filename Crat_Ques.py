import nltk, numpy as np, pandas as pd, re, os, random

# import torch

sentences = []
sent_labels = []

questions = ['what', 'which', 'when', 'how', 'list of', 'provide']  # 'tell me','show'

assist_verbs = ['is the', 'are the', 'has']

main_grups = ['site group','sitegroup', 'site', 'account', 'utility', 'bill', 'location', 'month', 'year','vendor']
main_grups_labels = ['sitegroup0','sitegroup0', 'site0', 'account0', 'utility0', 'bill0', 'location0', 'month0', 'year0','vendor0']
main_grup_dict={main_grups[i]:main_grups_labels[i] for i in range(len(main_grups))}
main_grup_dict['site group']= ['site_group0','site_group00']
main_grup_dict['and']='O'
main_grup_dict['of']='O'
main_grup_dict['for']='O';main_grup_dict['by']='O'


pronouns = ['having', 'has', 'for', 'in']

aggrA = ['highest', 'most', 'biggest', 'largest', 'smallest', 'least', 'maximum', 'max', 'min', 'minimum', 'average',
         'mean', 'sum', 'total', 'count', 'lowest', 'all']
aggrB = ['greater than', 'less than', 'smaller than', 'higher than', 'lower than', 'around', 'between', 'from',
         'above', 'below']

by_mains = ['cost', 'spend', 'usage', 'consumption', 'expend', 'kwh', 'gallons', 'kw', 'demand', 'peak kw', 'peak kwh',
            'dth']

utilities = ['electric', 'gas', 'sewer', 'trash', 'water']
# utilites_labels=['electric0', 'gas0', 'sewer0', 'trash0', 'water0']


locations = ['alabama', ' al', 'alaska', ' ak', 'arizona', ' az', 'arkansas', ' ar', 'california', ' ca', 'colorado',
             ' co', 'connecticut', ' ct', 'delaware', ' de', 'florida', ' fl', 'georgia', ' ga', 'hawaii', ' hi',
             'idaho', ' id', 'illinois', ' il', 'indiana', 'iowa', ' ia', 'kansas', ' ks', 'kentucky', 'ky',
             'louisiana', ' la', 'maine', ' me', 'maryland', ' md', 'massachusetts', ' ma', 'michigan', ' mi',
             'minnesota', ' mn', 'mississippi', ' ms', 'missouri', 'mo', 'montana', ' mt', 'nebraska', ' ne', 'nevada',
             ' nv', 'new hampshire', ' nh', 'new jersey', ' nj', 'new mexico', ' nm', 'new york', ' ny',
             'north carolina', 'nc', 'north dakota', ' nd', 'ohio', ' oh', 'oklahoma', ' ok', 'oregon', ' or',
             'pennsylvania', ' pa', 'rhode island', ' ri', 'south carolina', ' sc', 'south dakota', 'sd', 'tennessee',
             ' tn', 'texas', ' tx', 'utah', ' ut', 'vermont', ' vt', 'virginia', ' va', 'washington', ' wa',
             'west virginia', ' wv', 'wisconsin', 'wi', 'wyoming', ' wy']

months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

years = ['2017', '2018', '2019', '2020']


# function for adding individual accoount,site ,sitegroup  to main groups
def main_grup_with_ob(main_grup, ob,main_grup_label):
    if main_grup.__contains__('site group'):
        temp_var=main_grup.index('site group')
        main_grup[temp_var] = 'site group ' + ob
        main_grup_label=main_grup_dict['site group']+['site_group1']
    elif main_grup.__contains__('sitegroup'):
        temp_var = main_grup.index('sitegroup')
        main_grup[temp_var] = 'sitegroup ' + ob
        main_grup_label = [main_grup_dict['sitegroup']] + ['site_group1']
    elif main_grup.__contains__('site'):
        temp_var = main_grup.index('site')
        main_grup[temp_var] = 'site ' + ob
        main_grup_label=[main_grup_dict['site']] + ['site1']
    elif main_grup.__contains__('account'):
        temp_var = main_grup.index('account')
        main_grup[temp_var] = 'account ' + ob
        main_grup_label=[main_grup_dict['account']] + ['account1']
    elif main_grup.__contains__('vendor'):
        temp_var = main_grup.index('vendor')
        main_grup[temp_var] = 'vendor ' + ob
        main_grup_label = [main_grup_dict['vendor']] + ['vendor1']
    return main_grup,main_grup_label,temp_var



def label_generator(item, property,lent=1):
    item = ' '.join(item).split()
    item = ['O' for i in item]
    item[len(item) - 1] = property
    if lent>1:
        item[len(item) - 2] = property+'0'
        item[len(item) - 1] = property+'00'
    return item


def question_template(ques, object):
    aggregate_label = []
    utility_label = []
    location_label = []
    month_label = []
    year_label = []
    by_main_label = []
    main_grup_label = []

    random_selection = random.sample([0, 1], 1)[0]
    temp_num_check = 0

    if ques in ['what','which','how','where','when']:
        assist_verb = random.sample(['is the', 'are the'], 1)
        aggregate = random.sample(aggrA, random.randint(0, 1))
        by_main = random.sample(by_mains, 1)
        main_grup = random.sample(main_grups, random.randint(0, 3))
        month = random.sample(months, random.randint(0, 1))
        location = random.sample(locations, random.randint(0, 1))
        year = random.sample(years, random.randint(0, 1))
        utility = random.sample(utilities, random.randint(0, 1))

        # main_grup = ['year','site','site group']
        #
        # year = ['2019']
        year_and_mnth = False

        # Aggregate Settings
        if len(aggregate)>0:
            if aggregate[0] in ['highest', 'most', 'biggest', 'largest', 'maximum', 'max', 'average']:
                aggregate_label = ['max']
            elif aggregate[0] in ['smallest', 'least', 'min', 'minimum', 'lowest']:
                aggregate_label = ['min']
            elif aggregate[0] in ['number', 'count']:
                aggregate_label = ['count']
            elif aggregate[0] in ['average', 'mean']:
                aggregate_label = ['mean']
            elif aggregate[0] in ['total', 'sum', 'all']:
                aggregate_label = ['sum']

        # month Settings
        if main_grup.count('month') > 0:
            main_grup.remove('month')
            if main_grup.count('year') > 0:
                year_and_mnth = True
            if month.__len__() > 0:
                month = random.sample([' for the month  ', ' in the month '], 1) + random.sample(['', ' of '],
                                                                                                 1) + month
                month_label = label_generator(month, 'month1')
            else:
                month = random.sample([' for all months', ' months ', 'monthwise'], 1)
                month_label = label_generator(month, 'month0')
        elif month.__len__() > 0:
            month = random.sample([' for ', ' in '], 1) + month
            month_label = label_generator(month, 'month1')

        # Year Settings
        if main_grup.count('year') > 0:
            main_grup.remove('year')
            if year.__len__() > 0:
                if year_and_mnth:
                    year = ['and year ' + year[0]]
                year_label = label_generator(year, 'year1')
            else:
                year = random.sample([' for year', ' in year ', 'yearwise'], 1) + random.sample(['', ' of '],
                                                                                                1) + month
                year_label = label_generator(year, 'month1')
        elif year.__len__() > 0:
            # year = random.sample([' for ', 'in '], 0) + year
            year = random.sample([' for ', 'in '], 1) + year
            year_label = label_generator(year, 'year1')

        # Locations settings
        if len(location) > 0:
            if ''.join(location).split().__len__()>1:
                location_length=2
            else:
                location_length = 1

        if main_grup.count('location'):
            main_grup.remove('location')
            if len(location) > 0:
                location = random.sample([' for ', ' in '], 1) + random.sample(['location', 'state', 'area'],
                                                                               1) + location
                location_label = label_generator(location, 'location1',location_length)
            else:
                location = random.sample([' for all ', ' in all ', ' by '], 1) + random.sample(
                    ['locations', 'states', 'areas'], 1)
                location_label = label_generator(location, 'location0')
        elif len(location) > 0:
            location = random.sample([' for ', 'in '], 1) + location
            location_label = label_generator(location, 'location1',location_length)

        # By_groups settings
        if by_main[0] in ['kwh', 'kw',  'peak kw', 'peak kwh']:
            utility = random.sample(['electric'], random.randint(0, 1))
            if by_main[0] == 'kwh':
                by_main_label = ['usage_electric']
            elif by_main[0] == 'peak kwh':
                by_main_label = ['O','usage_electric']
            elif by_main[0] == 'kw':
                by_main_label = ['demand_electric']
            elif by_main[0] == 'peak kw':
                by_main_label = ['O','demand_electric']
            util = 'electric'
            temp_num_check = 1
        elif by_main[0] in ['dth', 'decatherm']:
            utility = random.sample(['gas', 'natural gas'], random.randint(0, 1))
            by_main_label = ['usage_gas']
            temp_num_check = 1
        elif by_main[0] in ['gal', 'gallons']:
            utility = random.sample(['water', 'sewer', 'trash'], random.randint(0, 2))
            by_main_label = ['usage_water']
            temp_num_check = 1

        if temp_num_check==0:
            if by_main[0] in ['cost','spend','expend']:
                by_main_label=['spend']
            elif by_main[0] =='demand':
                by_main_label = ['demand']
            else:
                by_main_label = ['usage']

        # Utility settings
        if main_grup.count('utility'):
            main_grup.remove('utility')
            if len(utility) > 0:
                utility = random.sample([' for ', ' by '], 1) + utility
                utility_label = label_generator(utility, 'utility1')
            elif temp_num_check == 1:
                utility = []
            else:
                utility = random.sample([' for all utilities ', ' by all utilities '], 1)
                utility_label = label_generator(utility, 'utility0')
        elif len(utility) > 0:
            utility = random.sample([' for ', 'by '], 1) + utility
            utility_label = label_generator(utility, 'utility1')


        # Main Group settings
        if main_grup.__len__()>0:
            if random_selection and main_grup in ['site group','sitegroup', 'site', 'account','vendor']:
                main_grup, main_grup_label,temp = main_grup_with_ob(main_grup, object,main_grup_label)
                temp=random.sample(['for', 'by','of'], 1) + [main_grup.pop(temp)]
                main_grup=' and '.join(main_grup).split()
                main_grup_label=['O']+main_grup_label+[main_grup_dict[i] for i in main_grup]
                main_grup=temp+main_grup
            else:
                if 'site group' in main_grup:
                    temp=main_grup.index('site group')
                    main_grup.pop(temp)
                    main_grup.insert(temp,'sitegroup')
                    main_grup= random.sample(['for', 'by','of'], 1)+' and '.join(main_grup).split()
                    temp = main_grup.index('sitegroup')
                    main_grup.pop(temp)
                    main_grup.insert(temp,'site group')
                else:
                    main_grup= random.sample(['for', 'by','of'], 1)+' and '.join(main_grup).split()

                main_grup_label += [main_grup_dict[i] for i in main_grup]
                temp_list=[]
                for i in main_grup_label:
                    if type(i) is str:
                        temp_list.append(i)
                    else:
                        for j in range(len(i)):
                            temp_list.append(i[j])
                main_grup_label=temp_list
        # if len(main_grup) > 0:
        #     if len(main_grup[0].split()) > 1:
        #         main_grup_label = [main_grup[0].split()[0] + '0', main_grup[0].split()[0] + '1']
        #     else:
        #         main_grup_label = [main_grup[0].split()[0] + '0']
        #     main_grup[0] = random.sample([' for ', 'of '], 1)[0] + main_grup[0]
        #     main_grup_label = ['O'] + main_grup_label
        # if len(main_grup) > 1 and len(main_grup) < 2:
        #     main_grup = [' and '.join(main_grup)]
        #     main_grup_label.append('O')
        #     main_grup_label.append(main_grup[1] + '0')
        # elif len(main_grup) > 2:
        #     main_grup = [' and '.join(main_grup)]
        #     main_grup_label.append('O')
        #     main_grup_label.append(main_grup[2] + '0')


        if (re.findall('are', assist_verb[0]).__len__() > 0) and len(main_grup) > 0:
            main_grup[0] = main_grup[0] + 's'
        if ques=='where':
            question_label=['location0']
            assist_verb_label=['O','O']
        elif ques=='when':
            question_label=['month0']
            assist_verb_label=['year0','O']
        else:
            question_label = ['O']
            assist_verb_label = ['O', 'O']




        sentence = [ques] + assist_verb + aggregate + by_main + main_grup + utility + month + year + location
        sent_label = question_label+assist_verb_label + aggregate_label + by_main_label + main_grup_label + utility_label + month_label + year_label + location_label
        x,y=len(sent_label),len(' '.join(sentence).split())
        # sentences.append(sentence)


        print(x,y)
        # print(sent_label)
        return ' '.join(sentence),sent_label

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
with open("sents.txt",'w') as sf:
    with open("labels.txt",'w') as sl:

        for i in range(100):
            #
            object = ''.join(random.sample(list('absdawqe!13213231#$@%231'), random.randint(1, 20)))
            ques=random.sample(['what','which','how','where','when'], 1)[0]
            a,b=  question_template(ques, object)
            sf.writelines(a+"\n")
            sl.writelines(str(b)+"\n")

    sl.close()
sf.close()

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
