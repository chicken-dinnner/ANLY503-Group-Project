#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 20:15:10 2018

@author: xintongzhao
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


df = pd.read_csv('/Users/xintongzhao/git/ANLY503/Raw_data/environmental.csv')
df = df[['State','Year','Data Item','Domain','Domain Category','Value']]
domain = (list(dict.fromkeys(list(df['Domain']))))
cols = list(df.columns)
#df = df.dropna(how = 'any')
df.head()
for col in cols:
    list_col = list(df[col])
    if type(list_col[0])==int:
        continue
    list_col = [i.replace('\t','') for i in list_col]
    list_col = [i.replace('\n','') for i in list_col]
    list_col = [i.replace(' ','') for i in list_col]
    df.loc[:,col]=list_col

value_list = list(df['Value'])
value_list = [i.replace(',','') for i in value_list]
value_list = [float(i) if i.isdigit()==True else np.nan for i in value_list]
df.loc[:,'Value']=value_list

#============================================================================
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

ax.set_title("Before: Data Records Distribution from each Year")

plt.show()






#============================================================================
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

plt.show()








#============================================================================

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
        

#df.to_csv('/Users/xintongzhao/git/ANLY503/cleaned_environmental_final.csv',index=False)

#============================================================================
#paired categorical plot
df = df[~df['Domain'].isin(['FERTILIZER'])]

import seaborn as sns
sns.set(style="whitegrid")

subdf = df[df['Domain']=='CHEMICAL,HERBICIDE']
# Set up a grid to plot survival probability against several variables
g = sns.PairGrid(subdf, y_vars="Value",
                 x_vars=["Year"],
                 height=10, aspect=1,size=5)

# Draw a seaborn pointplot onto each Axes
g.map(sns.pointplot, scale=1.3, errwidth=4, color="xkcd:plum")
g.fig.suptitle('Paired Categorical Plot for Chemical Use')
g.set(xlabel='Year', ylabel='Chemical Use Index')
sns.despine(fig=g.fig, left=True)



#============================================================================
#line chart
# Create a random dataset across several variables
dom = list(dict.fromkeys(df['Domain']))
subdf = pd.DataFrame(columns = ['CHEMICAL,FUNGICIDE'])

temp = df[df['Domain']=='CHEMICAL,FUNGICIDE']
subdf.loc[:,'CHEMICAL,FUNGICIDE']=list(temp['Value'])
# Use cubehelix to get a custom sequential palette
pal = sns.cubehelix_palette(subdf.shape[0], rot=-.5, dark=.3)


g = sns.violinplot(data=subdf, palette=pal, inner="points")
g.set_title('Violin Plot of Chemical Fungicide')
g.set_xlabel('Chemical type')
g.set_ylabel('Chemical Use Index',fontsize = 15)

#============================================================================
#boxplot
sns.set(style="ticks", palette="pastel")



# Draw a nested boxplot to show bills by day and time
g = sns.boxplot(x="Year", y="Value",
            hue="Domain", palette=["m", "g","r"],
            data=df)
g.set_title('Boxplot related with Environmental Factors')
g.set_xlabel('Year')
g.set_ylabel('Chemical Use Index',fontsize = 15)
sns.despine(offset=10, trim=True)













