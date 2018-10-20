#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd 
import matplotlib.pyplot as plt

def plot_incidence_mortality_count():
    df = pd.read_csv('../Raw_data/us_cancer_incidentandmoraloty_by_state.TXT',sep = '|')
    
    df = df[df['SITE']=='All Cancer Sites Combined']
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
    df['CRUDE_RATE'] = df['CRUDE_RATE'].astype(float)
    
    year = []
    count_sum =[]
    crude_rate = []
    pop = []
    for i in df['YEAR'].unique():
        df_sub = df[(df['YEAR'] == i) & (df['EVENT_TYPE']=='Mortality')]
        year.append(i)
        crude_rate.append(sum(df_sub['CRUDE_RATE'].multiply(df_sub['POPULATION']))/sum(df_sub['POPULATION']))
        count_sum.append(df_sub['COUNT'].sum())
        pop.append(df_sub['POPULATION'].sum())
    
    dfMortaloty_US = pd.DataFrame()
    dfMortaloty_US['YEAR'] = year
    dfMortaloty_US['POPULATION'] = pop
    dfMortaloty_US['COUNT'] = count_sum
    dfMortaloty_US['CRUDE_RATE'] = crude_rate
    dfMortaloty_US['EVENT_TYPE'] = 'Mortality'
    
    
    dfIncidence_US = df[(df['AREA'] == 'United States (comparable to ICD-O-2)')& 
                        (df['EVENT_TYPE'] == 'Incidence')][['YEAR',
                        'POPULATION','COUNT','CRUDE_RATE','EVENT_TYPE']]
    
    frames = [dfIncidence_US, dfMortaloty_US]
    df = pd.concat(frames)
    df['YEAR']=df['YEAR'].astype(int)
    
    fig, ax = plt.subplots()
    
    for key, grp in df.groupby(['EVENT_TYPE']):
        ax = grp.plot(ax = ax, x='YEAR', y='CRUDE_RATE',label = key)
    
    ax.set_title('Incidence Rate and Mortality Rate between 1999 and 2015')
    ax.set_ylabel('Number of Cases per 100,000 People')
    ax.set_xlabel('Year')
    
plot_incidence_mortality_count() 
