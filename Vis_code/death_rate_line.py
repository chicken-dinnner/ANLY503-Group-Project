#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd 
import sys

# This function will create a new variable called death rate by using 
# total death count / total incidence count for each year
def plot_death_rate():
    df_incidence = pd.read_csv('../Cleaned_data/cancer_incidence_us.csv')
    df_mortality = pd.read_csv('../Cleaned_data/cancer_mortality_us.csv')
    df_merge = pd.merge(df_incidence,df_mortality,on = 'YEAR')
    # create death rate 
    df_merge['Death_rate'] = df_merge['COUNT_y']/df_merge['COUNT_x']
    
    ax = df_merge.plot(x = 'YEAR',y='Death_rate',title = 'Death Rate across all Types of Cancers')
    
    ax.set_ylabel("Death Rate")

def main(argv):
    plot_death_rate()
    
if __name__ == "__main__":
    main(sys.argv)
    