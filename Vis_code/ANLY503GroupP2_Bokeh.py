#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 18:30:14 2018

@author: xintongzhao
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file

from scipy import stats
from bokeh.models import HoverTool



cancer = pd.read_csv('cancer_incidence_state.csv')
chem = pd.read_csv('cleaned_environmental.csv')
chem = chem[chem['Year']==2012]
cancer = cancer[cancer['YEAR']==2012]
cancer = cancer.sort_values(by='AREA',ascending = True)
chem = chem.sort_values(by='State',ascending = True)

states = list(dict.fromkeys(chem['State']))

states = [i[0]+i[1:].lower() for i in states]
cancer = cancer[cancer['AREA'].isin(states)]
cancer_rt = list(cancer['AGE_ADJUSTED_RATE'])
cancer_percent = []
for i in cancer_rt:
    score = stats.percentileofscore(cancer['AGE_ADJUSTED_RATE'], i, kind='rank')
    cancer_percent += [score]

states = list(cancer['AREA'])
states = [i.upper() for i in states]
chem = chem[chem['State'].isin(states)]

chem_value = []
for state in states:
    temp = chem[chem['State']==state]
    value = sum(list(temp['Value']))
    chem_value+=[value]
percent = []
for i in chem_value:
    score = stats.percentileofscore(chem['Value'], i, kind='rank')
    percent+=[score]

percent = [round(i,2) for i in percent]


final = pd.DataFrame(columns = ['state','chem','chem_percent','cancer','cancer_percent'])
final.loc[:,'state']=states
final.loc[:,'chem'] = chem_value
final.loc[:,'chem_percent']=percent
final.loc[:,'cancer']=cancer_rt
final.loc[:,'cancer_percent']=cancer_percent

chem_percent = []
for i in chem_value:
    score = stats.percentileofscore(final['chem'], i, kind='rank')
    chem_percent += [score]

final.loc[:,'chem_percent']=chem_percent

state = list(final['state'])
#x - cancer
#y - chem 
x_range = [min(cancer_rt),max(cancer_rt)]
y_range = [min(chem_value),max(chem_value)]

#N = 500
x = np.asarray(cancer_percent)
y = np.asarray(chem_percent)

z = [abs(i-j)/10 for i,j in zip(x,y)]



###############################Sub5-Figure1##################################
colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
]
radii = np.asarray(z)+0.1
from bokeh.plotting import ColumnDataSource
source = ColumnDataSource(data=dict(
    x=list(x),
    y=list(y),
    state=state,
    color = colors,
    radius = radii,
))


state = np.asarray(state)

N = 4000
#x = np.random.random(size=N) * 100
#y = np.random.random(size=N) * 100



TOOLS=TOOLS = "pan,wheel_zoom,reset,hover,save"

p = figure(title = "Relation between Chemical Use and Cancer Rate",tools=TOOLS)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("state", "@state"),
]

p.xaxis.axis_label = 'Percentile of Cancer Incidence among all States'
p.yaxis.axis_label = 'Percentile of Chemical Use among all States'


p.scatter(x='x', y='y', radius = 'radius',source = source,fill_color='color',alpha=0.6)
#p.circle('x', 'y', size=20, source=source)
output_file("color_scatter.html", title="color_scatter.py example")

show(p)  # open a browser


###############################Sub5-Figure2##################################

cancer = pd.read_csv('cancer_incidence_state.csv')
chem = pd.read_csv('cleaned_environmental.csv')

#######Dataframe########

TOOLS=TOOLS = "pan,wheel_zoom,reset,save,hover"


val_yr_chem =[]
years_chem = list(dict.fromkeys(chem['Year']))
for yr in years_chem:
    temp = chem[chem['Year']==yr]
    val = list(temp['Value'])
    val = sum(val)
    val_yr_chem+=[val]

val_yr_cancer = []
years_cancer = list(dict.fromkeys(cancer['YEAR']))
for yr in years_cancer:
    temp = cancer[cancer['YEAR']==yr]
    val = list(temp['COUNT'])
    val = sum(val)
    val_yr_cancer+=[val]

yr_chem = pd.DataFrame(columns = ['year','value'])
yr_chem['year']=years_chem
yr_chem['value']=val_yr_chem

yr_cancer = pd.DataFrame(columns=['year','value'])
yr_cancer['year']=years_cancer
yr_cancer['value']=val_yr_cancer
##############################Figure2

p1 = figure(x_axis_type="datetime", title="Cancer Trending 1999~2015",tools=TOOLS,plot_width=1000, plot_height=500)
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date (in Years)'
p1.yaxis.axis_label = 'Cancer Frequency Count (in thousands)'

hover = p.select_one(HoverTool)
hover.mode = 'vline'

source = ColumnDataSource(data=dict(
    year=list(yr_cancer['year'].astype(str)),
    value=list(yr_cancer['value']/1000),
))

p1.line(x ='year', y='value', color='#B2DF8A',line_width = 11,source=source)
output_file("bubble.html", title="bubble.py example")
show(p1)



##############################pre-fig3
pre_can = cancer.copy()
states = list(dict.fromkeys(pre_can['AREA']))

del pre_can['POPULATION']
del pre_can['AGE_ADJUSTED_RATE']
cols = ['YEAR']
yr = list(pre_can[pre_can['AREA']==states[0]]['YEAR'])
result = pd.DataFrame(columns = cols)
result['YEAR']=yr
for state in states:
    temp = pre_can[pre_can['AREA']==state]
    del temp['AREA']
    temp.columns=['YEAR',str(state).upper()]
    result = pd.merge(result,temp,on = 'YEAR',how='left')
    

    

##############################Figure3
from math import pi
import pandas as pd

from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.sampledata.unemployment1948 import data

result['YEAR'] = result['YEAR'].astype(str)
result = result.set_index('YEAR')
result.columns.name = 'States'

years = list(result.index)
states = list(result.columns)

# reshape to 1D array or rates with a month and year for each row.
df = pd.DataFrame(result.stack(), columns=['rate']).reset_index()

# this is the colormap from the original NYTimes plot
colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(palette=colors, low=df.rate.min(), high=df.rate.max())

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="US Cancer Frequency ({0} - {1})".format(years[0], years[-1]),
           x_range=years, y_range=list(reversed(states)),
           x_axis_location="above", plot_width=900, plot_height=800,
           tools=TOOLS, toolbar_location='below',
           tooltips=[('date', '@States @YEAR'), ('rate', '@rate')])

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x="YEAR", y="States", width=1, height=1,
       source=df,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')
output_file("correlation.html", title="correlation.py example")
show(p)      # show the plot


'''
# a chem
# b cancer

a = chem_value
b = cancer_rt
#y = np.linspace(y_range[0], y_range[1], N)
xx, yy = np.meshgrid(sorted(x), sorted(y))
d = np.zeros((40,40))-2
#d[:] = np.nan
for i in range(40):
    d[int(x[i]/2.5-1)][int(y[i]/2.5-1)] = z[i]





p = figure(x_range=(0,100), y_range=(0,100))

# must give a vector of image data for image parameter
p.image(image=[d], x=0, y=0, dw=100, dh=100, palette="Spectral11")
p.add_tools(HoverTool(tooltips=[("Cancer", "$x"), ("Chemical", "$y"), ("Percentile", "@image")]))
output_file("fff.html", title="image.py example")

show(p)  # open a browser
'''

'''
from math import pi
import pandas as pd

from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure
from bokeh.sampledata.unemployment1948 import data

data['Year'] = data['Year'].astype(str)
data = data.set_index('Year')
data.drop('Annual', axis=1, inplace=True)
data.columns.name = 'Month'

years = list(data.index)
months = list(data.columns)

# reshape to 1D array or rates with a month and year for each row.
df = pd.DataFrame(data.stack(), columns=['rate']).reset_index()

# this is the colormap from the original NYTimes plot
colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(palette=colors, low=df.rate.min(), high=df.rate.max())

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="US Unemployment ({0} - {1})".format(years[0], years[-1]),
           x_range=years, y_range=list(reversed(months)),
           x_axis_location="above", plot_width=900, plot_height=400,
           tools=TOOLS, toolbar_location='below',
           tooltips=[('date', '@Month @Year'), ('rate', '@rate%')])

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x="Year", y="Month", width=1, height=1,
       source=df,
       fill_color={'field': 'rate', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(colors)),
                     formatter=PrintfTickFormatter(format="%d%%"),
                     label_standoff=6, border_line_color=None, location=(0, 0))
p.add_layout(color_bar, 'right')

show(p)      # show the plot

'''