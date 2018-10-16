#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import seaborn as sns
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

# This file will 

def prepData():
    
    yearRange = list(range(1999,2016))

    df = pd.DataFrame()
    tokeep = ['Air Pollution','Chronic Drinking','Diabetes','Obesity','Smoking','Frequent Mental Distress',
              'Personal Income, Per Capita ','Income Inequity','Median Household Income','Excessive Drinking']
    for y in yearRange:
        inputName = "../Raw_data/"+str(y)+'-Annual.csv'
        df1 = pd.read_csv(inputName)
        dftokeep = df1[df1['Measure Name'].isin(tokeep)][['Edition','Measure Name',
                       'State Name', 'Rank', 'Value']]
        frames = [df, dftokeep]
        df = pd.concat(frames)
    
    df_health = df.copy()
    df_sub = df_health[(df_health['Measure Name']=='Median Household Income')|
                       (df_health['Measure Name']=='Smoking')|
                       (df_health['Measure Name']=='Diabetes')|
                       (df_health['Measure Name']=='Obesity')|
                       (df_health['Measure Name']=='Income Inequity')]
    
    # Check for missing values in each 
    for i in df_sub['State Name'].unique():
        for j in df_sub['Measure Name'].unique():
            if len(df_sub[(df_sub['State Name']==i)&(df_sub['Measure Name']==j)])!= 17:
                print('Missing value is ',i,j)
    
    # Income inequality in DC is missing in 2015. We use 2014 data to replace the missing value
    toadd =df_sub[(df_sub['State Name']=='District of Columbia')&
           (df_sub['Edition']==2014)&(df_sub['Measure Name']=='Income Inequity')]['Value'].values
    dftemp = pd.DataFrame([[2015,'Income Inequity','District of Columbia',np.nan,float(toadd)]], columns=list(df_sub.columns))
    df_sub = df_sub.append(dftemp, ignore_index=True)
#    df_sub.loc[-1] = [[2015,'Income Inequity','District of Columbia',np.nan,float(toadd)]]
#    df_sub.index = df_sub.index + 1  # shifting index
#    df_sub = df_sub.sort_index()
    df_sub['Value']= df_sub['Value'].astype(float)
    
    df_sub.to_csv('../Cleaned_data/health_annual.csv',index = False)   
    return(df_sub)

def plot_income(df_sub):
    plt.figure()
    sns.set(style="whitegrid")
    df_income = df_sub[df_sub['Measure Name']=='Median Household Income']
    
    ax = sns.boxplot(x="Measure Name", y="Value", data=df_income)
    ax.set_title('Boxplot of Household Income')
    ax.set_xlabel('Variable Name')

def plot_others(df_sub):
    plt.figure()
    sns.set(style="whitegrid")
    df_others = df_sub[df_sub['Measure Name']!='Median Household Income']
    ax1 = sns.boxplot(x="Measure Name", y="Value", data=df_others)
    ax1.set_title('Boxplot of all other variables')
    ax1.set_xlabel('Variable Name')
    

df_sub = prepData()
plot_income(df_sub)
plot_others(df_sub)

