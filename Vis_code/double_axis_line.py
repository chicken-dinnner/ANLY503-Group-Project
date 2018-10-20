#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter
from matplotlib import ticker




def cancerDF(df):
    
    cancer = pd.read_csv('../Cleaned_data/cancer_incidence_us.csv')
    
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
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    lns1 = ax.plot(cancer["YEAR"], cancer["COUNT"],label = "Number of Incidences")
    ax2 = ax.twinx()
    lns2 = ax2.plot(cancer["YEAR"], cancer["Value"],  color="r",label = "Chemical Use")
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=0)
    ax.set_ylabel('Number of Cancer Incidences',fontsize=8)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax.set_title('Relationship between Cancer Incidence Number and Chemical Use',fontsize=12)
    ax2.set_ylabel('Chemical Use Value',fontsize = 8)
    ax.set_xlabel("Year")
    
    plt.show()
    
if __name__ == "__main__":

    df = pd.read_csv('../Cleaned_data/cleaned_environmental.csv')
    cancer = cancerDF(df)
    linechart(df,cancer)




