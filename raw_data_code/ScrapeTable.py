#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 13:16:37 2018

@author: xintongzhao
"""
import requests
import lxml.html as lh
import pandas as pd


def scrape(url):
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        print('%d:"%s"'%(i,name))
        col.append((name,[]))
        
        
        
    #Since out first row is the header, data is stored on the second rowonwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        
        #If row is not of size 10, the //tr data is not from our table 
        if len(T)!=21:
            break
        
        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1
        
        
        
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    #df.to_csv('environmental.csv',index=False)
    return df
    
def cleanDF(df):
    df = df[['Year','State','Commodity','Data Item','Domain','Domain Category','Value','CV (%)']]
    cols = list(df)
    for col in cols:
        col_temp = list(df[col])
        col_temp = [str(element).replace('\n','') for element in col_temp]
        col_temp = [str(element).replace('\t','') for element in col_temp]
        col_temp = [str(element).replace(' ','') for element in col_temp]
        if col == 'Value':
            col_temp = [i.replace('(D)','0') for i in col_temp]
            col_temp = [i.replace('(Z)','0') for i in col_temp]
            col_temp = [i.replace(',','') for i in col_temp]
            col_temp = [int(i) for i in col_temp]
        df[col]=col_temp
    return df


if __name__ == "__main__":
    url = 'https://quickstats.nass.usda.gov/data/printable/7317E7AF-C611-3906-8D35-2EABF24E1487'
    print("Scraping data from given url...")
    df = scrape(url)
    print("Web scraping complete.")
    df = cleanDF(df)
    df.to_csv('cleaned_environmental.csv',index=False)
    print('DataFrame Cleaned.')
    