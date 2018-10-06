#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd 

def clean_US_mortaloty():
    df = pd.read_csv('us_cancer_mortaloty.csv')
    df = df[df['Data Type'] == 'U.S. Mortality']
    df = df.drop(columns=['Modeled Rate'])
    df.to_csv('cancer_mortaloty_us.csv',index = False)

if __name__ == "__main__":
    clean_US_mortaloty()