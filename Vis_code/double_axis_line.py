#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 17:01:46 2018

@author: xintongzhao
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def cancerDF(df):
    
    cancer = pd.read_csv('/Users/xintongzhao/git/ANLY503/Cleaned_data/cancer_incidence_us.csv')
    
    yrs = sorted(list(set(list(df['Year']))))
    
    cancer = cancer[cancer['YEAR'].isin(yrs)]
    
    cancer = cancer[['YEAR','COUNT']]
    mrge_df = df[df['Year'].isin(list(cancer['YEAR']))]
    sumV = []
    for j in sorted(list(cancer['YEAR'])):
        l = list(mrge_df[mrge_df['Year'].isin([j])]['Value'])
        v = sum(l)
        sumV+=[v]
        
    cancer.loc[:,'Value'] = sumV
    cancer = cancer[cancer['YEAR'].isin(yrs)]
    return cancer


def linechart(df,cancer):
    #============================================================================
    
    
    
    ax = cancer.plot(x="YEAR", y="COUNT", legend=False,label = "Number of Incidences")
    ax.set_ylabel('Number of Cancer Incidences',fontsize=15)
    ax2 = ax.twinx()
    ax2.set_ylabel('Chemical Use Value',fontsize = 15)
    ax2 = cancer.plot(x="YEAR", y="Value", ax=ax2, legend=False, color="r",label = "Chemical Use")
    ax.figure.legend()
    ax.set_title('Relationship between Cancer Incidence Number and Chemical Use',fontsize=15)
    ax.set_xlable("Year")
    
    plt.show()
    
if __name__ == "__main__":

    df = pd.read_csv('cleaned_environmental.csv')
    cancer = cancerDF(df)
    linechart(df,cancer)




