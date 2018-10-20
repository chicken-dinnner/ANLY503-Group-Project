import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../Raw_data/us_cancer_incidentandmoraloty_by_state.TXT',sep = '|')

df = df[df['SITE']=='All Cancer Sites Combined']
df = df[df['RACE'] =='All Races']
df = df[df['SEX']=='Male and Female']
df = df[df['YEAR']!='2011-2015']


State = ['Alabama', 'Alaska', 'Arizona', 'Arkansas',
       'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 
       'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
       'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
       'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 
       'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
       'New Jersey', 'New Mexico', 'New York', 'North Carolina',
       'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
       'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
       'Texas', 'Utah','Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 
       'Wyoming','United States (comparable to ICD-O-2)']


df = df[df['AREA'].isin(State)]
df['AGE_ADJUSTED_RATE'] = df['AGE_ADJUSTED_RATE'].astype(float)
df['COUNT'] = df['COUNT'].astype(float)



# check for missing values 
print("Check missing areas for incidence rate",set(State)-set(df[df['EVENT_TYPE']=='Incidence']['AREA'].unique()))
print("Check missing areas for mortality rate",set(State)-set(df[df['EVENT_TYPE']=='Mortality']['AREA'].unique()))

for state in State:
    df_state = df[df['AREA']==state]
    incidence_missing = set(range(1999,2011))-set(df_state[df_state['EVENT_TYPE']=='Incidence']['YEAR'].astype(int))
    mortality_missing = set(range(1999,2011))-set(df_state[df_state['EVENT_TYPE']=='Incidence']['YEAR'].astype(int))
    if (len(incidence_missing)!= 0):
        print("State: ", state, "incidence rate is missing for years of ", set(incidence_missing))
    if (len(mortality_missing)!= 0):
        print("State: ", state, "mortality rate is missing for years of ", set(mortality_missing))

year = []
count_sum =[]
age_adj_rate = []
pop = []
for i in df['YEAR'].unique():
    df_sub = df[(df['YEAR'] == i) & (df['EVENT_TYPE']=='Mortality')]
    year.append(i)
    age_adj_rate.append(sum(df_sub['AGE_ADJUSTED_RATE'].multiply(df_sub['POPULATION']))/sum(df_sub['POPULATION']))
    count_sum.append(df_sub['COUNT'].sum())
    pop.append(df_sub['POPULATION'].sum())

dfMortaloty_US = pd.DataFrame()
dfMortaloty_US['YEAR'] = year
dfMortaloty_US['POPULATION'] = pop
dfMortaloty_US['COUNT'] = count_sum
dfMortaloty_US['AGE_ADJUSTED_RATE'] = age_adj_rate
dfMortaloty_US['EVENT_TYPE'] = 'Mortality'


dfIncidence_US = df[(df['AREA'] == 'United States (comparable to ICD-O-2)')& 
                    (df['EVENT_TYPE'] == 'Incidence')][['YEAR',
                    'POPULATION','COUNT','AGE_ADJUSTED_RATE']]

dfIncidence_State = df[(df['AREA'] != 'United States (comparable to ICD-O-2)')& 
                    (df['EVENT_TYPE'] == 'Incidence')][['YEAR',
                    'POPULATION','COUNT','AGE_ADJUSTED_RATE','AREA']]

dfMortaloty_State = df[(df['AREA'] != 'United States (comparable to ICD-O-2)')& 
                    (df['EVENT_TYPE'] == 'Mortality')][['YEAR',
                    'POPULATION','COUNT','AGE_ADJUSTED_RATE','AREA']]


df_incidence = df[ (df['EVENT_TYPE'] == 'Incidence')][['YEAR','POPULATION',
                  'COUNT','AGE_ADJUSTED_RATE','AREA']]
df_mortality = df[ (df['EVENT_TYPE'] == 'Mortality')][['YEAR','POPULATION',
                  'COUNT','AGE_ADJUSTED_RATE','AREA']]

plt.figure(figsize=(8,6))
plt.plot(df_incidence.YEAR.astype(int), df_incidence.AGE_ADJUSTED_RATE, 'o', color='black')
plt.xlabel('Year')
plt.ylabel('Age Adjusted Rate')
plt.title('Scatter Plot of Incidence Age Adjusted Rate')

plt.figure(figsize=(8,6))
plt.plot(df_mortality.YEAR.astype(int), df_mortality.AGE_ADJUSTED_RATE, 'o', color='black')
plt.xlabel('Year')
plt.ylabel('Age Adjusted Rate')
plt.title('Scatter Plot of Mortality Age Adjusted Rate')

dfIncidence_US.to_csv('../Cleaned_data/cancer_incidence_us.csv',index = False)
dfMortaloty_US.to_csv('../Cleaned_data/cancer_mortality_us.csv',index = False)
dfIncidence_State.to_csv('../Cleaned_data/cancer_incidence_state.csv',index = False)
dfMortaloty_State.to_csv('../Cleaned_data/cancer_mortality_state.csv',index = False)