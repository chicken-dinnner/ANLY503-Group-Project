#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 15:25:47 2018

@author: xintongzhao
"""
import pandas as pd
#paired categorical plot
def paired_categ(df):
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


if __name__ == "__main__":
    df = pd.read_csv('cleaned_environmental.csv')
    paired_categ(df)