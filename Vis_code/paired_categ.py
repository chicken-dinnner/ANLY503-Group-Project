#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#paired categorical plot

def paired_categ(df):
    
    sns.set(style="whitegrid")

    
    subdf = df[df['Domain']=='CHEMICAL,HERBICIDE']
    # Set up a grid to plot survival probability against several variables
    g = sns.PairGrid(subdf, y_vars="Value",
                     x_vars=["Year"],
                     aspect=1,size=7)
    
    # Draw a seaborn pointplot onto each Axes
    g.map(sns.pointplot, scale=1.3, errwidth=3, color="xkcd:plum")
    g.fig.suptitle('Paired Categorical Plot for Chemical Use')
    g.set(xlabel='Year', ylabel='Chemical Use Index')
    sns.despine(fig=g.fig, left=True)


if __name__ == "__main__":
    df = pd.read_csv('../Cleaned_data/cleaned_environmental.csv')
    paired_categ(df)