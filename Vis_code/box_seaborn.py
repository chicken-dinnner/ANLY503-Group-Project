#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def box_seaborn(df):
    #============================================================================
    #boxplot
    sns.set(style="ticks", palette="pastel")
    
    
    plt.figure(figsize=(8,6))
    # Draw a nested boxplot to show bills by day and time
    g = sns.boxplot(x="Year", y="Value",
                hue="Domain", palette=["m", "g","r"],
                data=df)
    g.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    g.set_title('Range of Different Chemical Uses',fontsize = 12)
    g.set_xlabel('Year',fontsize =10)
    g.set_ylabel('Chemical Use Index',fontsize = 10)
    
    sns.despine(offset=10, trim=True)

    
if __name__ == "__main__":
    df = pd.read_csv('../Cleaned_data/cleaned_environmental.csv')
    box_seaborn(df)