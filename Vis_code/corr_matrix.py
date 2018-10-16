#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# This function will compute correlation score among age adjusted rate, median
# household income, smoking, diabetes and obesity

def get_corr_matrix():
    sns.set(style="white")
    
    df_incidence = pd.read_csv('../Cleaned_data/cancer_incidence_state.csv')
    df_health = pd.read_csv('../Cleaned_data/health_annual.csv')

    df_merge = pd.merge(df_incidence,df_health, left_on = ['AREA','YEAR'],
             right_on = ['State Name','Edition'])
    
    
    
    df_corr = pd.DataFrame()
    df_corr['Income'] = df_merge[df_merge['Measure Name']=='Median Household Income']['Value'].tolist()
    df_corr['Smoking'] = df_merge[df_merge['Measure Name']=='Smoking']['Value'].tolist()
    df_corr['Diabetes'] = df_merge[df_merge['Measure Name']=='Diabetes']['Value'].tolist()
    df_corr['Obesity'] = df_merge[df_merge['Measure Name']=='Obesity']['Value'].tolist()
    df_corr['Income Inequity'] = df_merge[df_merge['Measure Name']=='Income Inequity']['Value'].tolist()
    df_corr['Age_adj_rate'] = df_merge[df_merge['Measure Name']=='Diabetes']['AGE_ADJUSTED_RATE'].tolist()
    
    corr = df_corr.corr()
    ax = sns.heatmap(corr,cmap="YlGnBu",annot=True)
    ax.set_title('Correlation Plot of Cancer Incidence Rate')
    
def main(argv):
    get_corr_matrix()
    
if __name__ == "__main__":
    main(sys.argv)
    