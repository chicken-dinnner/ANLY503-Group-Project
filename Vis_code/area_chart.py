#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:35:16 2018

@author: FrankWang
"""

import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('../Raw_data/us_cancer_incidentandmoraloty_by_state.TXT',sep = '|')


df = df[df['RACE'] =='All Races']
df = df[df['SEX']=='Male and Female']
df = df[df['YEAR']!='2011-2015']

State = ['Alabama', 'Alaska', 'Arizona', 'Arkansas',
       'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 
       'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
       'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
       'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 
       'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
       'New Jersey', 'New Mexico', 'New York', 'North Carolina',
       'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
       'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
       'Texas', 'Utah','Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 
       'Wyoming','United States (comparable to ICD-O-2)']
df = df[df['AREA'].isin(State)]


df_prostate = df.loc[(df['SITE'] =='Prostate') & (df['EVENT_TYPE']=='Incidence'),:]
df_lung = df.loc[(df['SITE'] =='Lung and Bronchus')& (df['EVENT_TYPE']=='Incidence'),:]
df_breast = df.loc[(df['SITE'] =='Female Breast')& (df['EVENT_TYPE']=='Incidence'),:]
df_prostate['COUNT'] = df_prostate['COUNT'].astype(int)
df_lung['COUNT'] = df_lung['COUNT'].astype(int)
df_breast['COUNT'] = df_breast['COUNT'].astype(int)


prostate_count = df_prostate.groupby('YEAR')['COUNT'].sum().tolist()
lung_count = df_lung.groupby('YEAR')['COUNT'].sum().tolist()
breast_count = df_breast.groupby('YEAR')['COUNT'].sum().tolist()

df_tot = pd.read_csv('../Cleaned_data/cancer_incidence_us.csv')
tot_count = df_tot.COUNT
other_count = [i-j-k-z for i,j,k,z in zip(tot_count,prostate_count,lung_count,breast_count)]

df_prostate = df.loc[(df['SITE'] =='Prostate') & (df['EVENT_TYPE']=='Mortality'),:]
df_lung = df.loc[(df['SITE'] =='Lung and Bronchus')& (df['EVENT_TYPE']=='Mortality'),:]
df_breast = df.loc[(df['SITE'] =='Female Breast')& (df['EVENT_TYPE']=='Mortality'),:]
df_prostate['COUNT'] = df_prostate['COUNT'].astype(int)
df_lung['COUNT'] = df_lung['COUNT'].astype(int)
df_breast['COUNT'] = df_breast['COUNT'].astype(int)

prostate_count_mortality = df_prostate.groupby('YEAR')['COUNT'].sum().tolist()
lung_count_mortality = df_lung.groupby('YEAR')['COUNT'].sum().tolist()
breast_count_mortality = df_breast.groupby('YEAR')['COUNT'].sum().tolist()

df_tot = pd.read_csv('../Cleaned_data/cancer_mortality_us.csv')
tot_count_mortality = df_tot.COUNT
other_count_mortality = [i-j-k-z for i,j,k,z in zip(tot_count_mortality,prostate_count_mortality,lung_count_mortality,breast_count_mortality)]


f = plt.figure(figsize=(10,15))
ax = f.add_subplot(211)
ax2 = f.add_subplot(212)
x=list(range(1999,2016))
y=[prostate_count,lung_count,breast_count,other_count]
 
# Basic stacked area chart.
ax.stackplot(x,y, labels=['Number of Incidences of Prostate Cancer',
                           'Number of Incidences of Lung Cancer',
                           'Number of Incidences of Breast Cancer',
                           'Number of Incidences of Other Cancers'])
ax.legend(loc='upper left')
ax.set_ylim([0,2000000])
ax.set_xlabel('Year')

ax.set_ylabel('Number of Incidences')
ax.set_title('Number of Incidences of Different Types of Cancers between 1999 and 2015')

ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

y=[prostate_count_mortality,lung_count_mortality,breast_count_mortality,other_count_mortality]

# Basic stacked area chart.
ax2.stackplot(x,y, labels=['Number of Mortalities of Prostate Cancer',
                           'Number of Mortalities of Lung Cancer',
                           'Number of Mortalities of Breast Cancer',
                           'Number of Mortalities of Other Cancers'])
ax2.legend(loc='upper left')
ax2.set_ylim([0,700000])
ax2.set_xlabel('Year')
ax2.set_ylabel('Number of Mortalities')
ax2.set_title('Number of Mortalities of Different Types of Cancers between 1999 and 2015')

ax2.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
