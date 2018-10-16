#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 16:57:41 2018

@author: xintongzhao
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def violin(df):
    #============================================================================
    #Violin chart
    # Create a random dataset across several variables
    subdf = pd.DataFrame(columns = ['CHEMICAL,FUNGICIDE'])
    
    temp = df[df['Domain']=='CHEMICAL,FUNGICIDE']
    subdf.loc[:,'CHEMICAL,FUNGICIDE']=list(temp['Value'])
    # Use cubehelix to get a custom sequential palette
    pal = sns.cubehelix_palette(subdf.shape[0], rot=-.5, dark=.3)
    
    
    g = sns.violinplot(data=subdf, palette=pal, inner="points")
    g.set_title('Violin Plot of Chemical Fungicide')
    g.set_xlabel('Chemical type')
    g.set_ylabel('Chemical Use Index',fontsize = 15)
    
    
if __name__ == "__main__":
    df = pd.read_csv('cleaned_environmental.csv')
    violin(df)