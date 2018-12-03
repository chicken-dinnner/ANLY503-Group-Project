#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 20:15:10 2018

@author: xintongzhao
"""
#load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#load raw dataframe to prepare for data cleaning
df = pd.read_csv('/Users/xintongzhao/git/ANLY503/Raw_data/environmental.csv')
#keep wanted columns only
df = df[['State','Year','Data Item','Domain','Domain Category','Value']]
#get a list of values under column 'domain'
domain = (list(dict.fromkeys(list(df['Domain']))))
#get columns
cols = list(df.columns)
#df = df.dropna(how = 'any')
print('Below are first few rows from dataframe:\n')
df.head()


#============================================================================
#Start cleaning: remove all noisy characters such as '\t','\n' or empty space
for col in cols:
    list_col = list(df[col])
    if type(list_col[0])==int:
        continue
    list_col = [i.replace('\t','') for i in list_col]
    list_col = [i.replace('\n','') for i in list_col]
    list_col = [i.replace(' ','') for i in list_col]
    df.loc[:,col]=list_col

#Then, we convert numbers in string format back to float for further use
value_list = list(df['Value'])
#replace comma in string
value_list = [i.replace(',','') for i in value_list]
#convert to float
value_list = [float(i) if i.isdigit()==True else np.nan for i in value_list]
#write back to the dataframe
df.loc[:,'Value']=value_list

#============================================================================
#Start visualization for data cleaning phase
#first calculate number of records under each year
yrs = list(dict.fromkeys(df['Year']))
yr1 = len(list(df[df['Year']==yrs[0]]['Domain']))
yr2 = len(list(df[df['Year']==yrs[1]]['Domain']))
yr3 = len(list(df[df['Year']==yrs[2]]['Domain']))
yr4 = len(list(df[df['Year']==yrs[3]]['Domain']))



#Visualize: Pie chart
#this pie chart is designed to show the weight distribution of data from each year
#If the distribution is not similar with equally distributed then we need to make 
#then equal
fig, ax = plt.subplots(figsize=(8, 12), subplot_kw=dict(aspect="equal"))

recipe = ["%s 1997"%(yr1),
          "%s 2002"%(yr2),
          "%s 2007"%(yr3),
          "%s 2012"%(yr4)]

data = [int(x.split()[0]) for x in recipe]
ingredients = [x.split()[-1] for x in recipe]


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} Records)".format(pct, absolute)


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, ingredients,
          title="Years",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Before: Data Records Distribution from each Year")

plt.show()


#============================================================================
#Further cleaning: Keep wanted sub-categories under domain category only
#Remove rows from year 2013 since the categories from 2013 do not match those
#from other year
df = df.drop_duplicates(subset=list(df),keep='first')
df = df[~df['Year'].isin([2013])]

total_list=['CHEMICAL,FUNGICIDE:(TOTAL)',
            'CHEMICAL,HERBICIDE:(TOTAL)','CHEMICAL,OTHER:(TOTAL)','CHEMICAL:(TOTAL)','FERTILIZER:(TOTAL)']
df = df[df['Domain Category'].isin(total_list)]
ditem = list(dict.fromkeys(df['Data Item']))
ditem = [i for i in ditem if 'MEASUREDINACRES' in i]
df = df[~df['Data Item'].isin(ditem)]

df = df.reset_index()

#============================================================================
#Visualization: Pie chart part 2
#this shows the distribution after cleanning
yrs = list(dict.fromkeys(df['Year']))
yr1 = len(list(df[df['Year']==yrs[0]]['Domain']))
yr2 = len(list(df[df['Year']==yrs[1]]['Domain']))
yr3 = len(list(df[df['Year']==yrs[2]]['Domain']))
yr4 = len(list(df[df['Year']==yrs[3]]['Domain']))

fig, ax = plt.subplots(figsize=(8, 12), subplot_kw=dict(aspect="equal"))

recipe = ["%s 1997"%(yr1),
          "%s 2002"%(yr2),
          "%s 2007"%(yr3),
          "%s 2012"%(yr4)]

data = [int(x.split()[0]) for x in recipe]
ingredients = [x.split()[-1] for x in recipe]


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} Records)".format(pct, absolute)


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, ingredients,
          title="Years",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("After: Data Records Distribution from each Year")
#show the chart
plt.show()

#============================================================================

#Prepare for the next visualization
#In order to show how the dataframe is cleanned, we pick one state as an example
#and then visualize its related data below
domains = (list(dict.fromkeys(list(df['Domain']))))
miss=[]
yrs = []
dom = []
years = list(dict.fromkeys(df['Year']))
for year in years:
    temp = df[df['Year'].isin([year])]
    for domain in domains:
        d_values = list(temp[temp['Domain'].isin([domain])]['Value'])
        na = len([i for i in d_values if np.isnan(i)==True])
        miss+=[na]
        yrs+=[year]
        dom+=[domain]

result = pd.DataFrame(columns=['Domain','Missing','Year'])
result.loc[:,'Domain']=dom
result.loc[:,'Missing']=miss
result.loc[:,'Year']=yrs
#df = df.dropna(how = 'any')


insect = df[df['Data Item']=='AGLAND-TREATED,MEASUREDINACRES']
miss_states = list(set(list(insect[insect['Value'].isin([np.nan])]['State'])))
miss_insect = insect[insect['State'].isin(['RHODEISLAND'])]

#============================================================================
#Continue visualization
#Histogram which displays the value of chemical use under each sub-categories
#This visualize data before cleanning
FUNGICIDE = (2416,2494,2736,0)
HERBICIDE = (7108,7121,8775,10645)
OTHER = (206,275,275,0)


ind = np.arange(len(HERBICIDE))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (15,10))
rects1 = ax.bar(ind, FUNGICIDE, width/2,
                color='SkyBlue', label='FUNGICIDE')
rects2 = ax.bar(ind + width/2, HERBICIDE, width/2,
                color='IndianRed', label='HERBICIDE')
rects3 = ax.bar(ind - width/2, OTHER, width/2,
                color='Green', label='OTHER')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Chemical Use Index')
ax.set_title('Before: Chemical in 3 Categories Per Year')
ax.set_xticks(ind)
ax.set_xlabel('Year')
ax.set_xticklabels(('1997', '2002', '2007', '2012'))
ax.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
plt.show()


#============================================================================
#Histogram cont'
#Shows data after cleaning

FUNGICIDE = (2416,2494,2736,2736)
HERBICIDE = (7108,7121,8775,10645)
OTHER = (206,275,275,275)


ind = np.arange(len(HERBICIDE))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize = (15,10))
rects1 = ax.bar(ind, FUNGICIDE, width/2,
                color='SkyBlue', label='FUNGICIDE')
rects2 = ax.bar(ind + width/2, HERBICIDE, width/2,
                color='IndianRed', label='HERBICIDE')
rects3 = ax.bar(ind - width/2, OTHER, width/2,
                color='Green', label='OTHER')
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Chemical Use Index')
ax.set_title('After: Chemical in 3 Categories Per Year')
ax.set_xticks(ind)
ax.set_xlabel('Year')
ax.set_xticklabels(('1997', '2002', '2007', '2012'))
ax.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
plt.show()

#============================================================================
#Final phase of data cleanning: fill empty values
#Once there is an empty data in the dataframe, we cannot use this record to 
#perform further task; However, if we simply remove the record, then this 
#action will affect on the total completeness of dataset.

#Since our data volumn is not large, in order to prevent potential data loss,
#we decide to fill in empty data by the data which has closest date to it.
#It could be the data value before/after the empty data, depends on which is closer.
types = list(dict.fromkeys(df['Domain']))

for state in miss_states:
    print(state,':\n')
    for typ in types:
        print(typ)
        temp = df[df['State']==state]
        values = list(temp[temp['Domain'].isin([typ])]['Value'])
        while True in [np.isnan(i) for i in values]:
            print('True')
            idx_na = [str(i) for i in values].index('nan')
            idx = idx_na
            idx_df = temp[temp['Value'].isna()].index[0]
            print(idx)
            try:
                while True:
                    if np.isnan(values[idx])==False:
                        break
                    idx=idx-1
            except:
                while True:
                    if np.isnan(values[idx])==False:
                        break             
                    idx=idx+1
            print(idx)
            values[idx_na]=values[idx]
                
        #values = [values[idx] if np.isnan(i)==True else i for i in values]

            df.iloc[idx_df,6] = values[idx]

#finally, we remove all category about fertilizer since it is not related with 
#our study.
df = df[~df['Domain'].isin(['FERTILIZER'])]
#Data cleaning ends here.
#At last, we save the cleaned dataframe to local computer.
df.to_csv('/Users/xintongzhao/git/ANLY503/cleaned_environmental.csv',index=False)

#============================================================================








