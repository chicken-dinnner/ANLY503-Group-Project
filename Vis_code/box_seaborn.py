#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 16:59:12 2018

@author: xintongzhao
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def box_seaborn(df):
    #============================================================================
    #boxplot
    sns.set(style="ticks", palette="pastel")
    
    
    plt.figure(figsize=(15,8))
    # Draw a nested boxplot to show bills by day and time
    g = sns.boxplot(x="Year", y="Value",
                hue="Domain", palette=["m", "g","r"],
                data=df)
    g.set_title('Boxplot related with Environmental Factors',fontsize = 15)
    g.set_xlabel('Year',fontsize =15)
    g.set_ylabel('Chemical Use Index',fontsize = 15)
    
    sns.despine(offset=10, trim=True)

    
if __name__ == "__main__":
    df = pd.read_csv('cleaned_environmental.csv')
    box_seaborn(df)