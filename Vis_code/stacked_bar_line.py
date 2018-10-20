#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib import rc
import matplotlib.ticker as ticker


def plot_incidence(df_incidence):
    x = list(range(1999,2016))
    rc('mathtext', default='regular')
    
    fig = plt.figure(figsize=(8,12))
    ax = fig.add_subplot(211)
    
    
    
    ax.bar(x, df_incidence['COUNT'],label='Number of Incidences')
    ax1 = ax.twinx()
    ax1.plot(x, df_incidence['AGE_ADJUSTED_RATE'].tolist(),'-r', label='Age Adjusted Rate')
    ax.set_xlabel('Year')
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%1.0f'))
    ax.set_ylabel('Number of Incidences')
    ax1.set_ylabel('Age Adjusted Rate')
    ax.set_title('Cancer Incidences')
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax1.set_ylim([250,530])
    ax.set_ylim([700000,2000000])
    ax.legend(loc=0)
    ax1.legend(loc=2)
    
    


def plot_mortality(df_mortality):
    x = list(range(1999,2016))
    rc('mathtext', default='regular')
    fig = plt.figure(figsize=(8,12))
    ax = fig.add_subplot(211)
    ax.bar(x, df_mortality['COUNT'],label='Number of Mortalities')
    ax1 = ax.twinx()
    ax1.plot(x, df_mortality['AGE_ADJUSTED_RATE'].tolist(),'-r', label='Age Adjusted Rate')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Mortalities')
    ax1.set_ylabel('Age Adjusted Rate')
    ax.set_title('Cancer Mortalities')
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%1.0f'))
    ax1.set_ylim([0,220])
    ax.set_ylim([450000,650000])
    ax.legend(loc='upper right')
    ax1.legend(loc='upper left')
    
    
    
df_incidence = pd.read_csv('../Cleaned_data/cancer_incidence_us.csv')
df_mortality = pd.read_csv('../Cleaned_data/cancer_mortality_us.csv')
plot_incidence(df_incidence)
plot_mortality(df_mortality)