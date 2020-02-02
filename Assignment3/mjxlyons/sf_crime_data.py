#module to load all the crime data

import pandas as pd

#load data
df = pd.read_csv('../datasets/Police_Department_Incidents_-_Previous_Year__2016_.csv')

#dropna of district
district_df = df.dropna(subset=['PdDistrict'])

#add bins of hours
hourBins = df['Time'].str.slice(stop=2)
df['TimeBins'] = hourBins

#get list of crimes
#drop non-criminal category
crime_df = df
crime_df = crime_df[crime_df.Category != 'NON-CRIMINAL']

#construct crime frequencies based on days
day_crimes = crime_df['DayOfWeek'].value_counts()
ordered_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_crimes = day_crimes.reindex(ordered_days)

#crime counts based on hour
hour_crimes = crime_df['TimeBins'].value_counts()

#ordered list of strings of numbers, 00 to 23, to sort hour_crimes
ordered_time = []
for i in range(24):
    str_i = str(i)
    if len(str_i) < 2:
        str_i = '0'+str_i
    ordered_time.append(str_i)
    
#reindex hour_crimes, to be in order of hours
hour_crimes = hour_crimes.reindex(ordered_time)

#################### SANKEY GRAPH ################################

#month list
month_list = ['Jan','Feb','Mar','Apr','May',"Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

#list of top 10 crimes
ten_df = crime_df.dropna(subset=['PdDistrict'])
crime_count = dict(ten_df['Category'].value_counts())
crimes_l = []
for crime in crime_count:
    crimes_l.append( (crime_count[crime], crime) )
crimes_l.sort(reverse = True)
ten_crimes =[]
for i in range(10):
    ten_crimes.append(crimes_l[i][1])

#reduce df to only the top 10 crimes
#https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
frames = []
for crime in ten_crimes:
    frames.append(ten_df[ten_df.Category == crime])
ten_df = pd.concat(frames)

#sankey labels: district, crime, resolution
district_labels =   list(ten_df['PdDistrict'].unique())
crime_labels =      list(ten_df['Category'].unique())
resolution_labels = list(ten_df['Resolution'].unique())
sankey_labels = district_labels + crime_labels + resolution_labels

#label offsets
crime_offset = len(district_labels)
resolution_offset = crime_offset + len(crime_labels)
    
#test
#print(crime_labels)
#print(ten_df.size)
#print(sankey_labels[resolution_offset])
#print(sankey_labels)
#print(district_df.size)

#mappings: source, target, value
#return sankey mappings, for that month
def sankeyMap(month):
    
    #mappings
    sank_source = []
    sank_target = []
    sank_value  = []
    for i in range(len(district_labels)):
        for j in range(len(crime_labels)):
            
            #source and target
            sank_source.append(i)
            sank_target.append(j + crime_offset)
            
            #value
            inter_df = ten_df[ten_df.PdDistrict == district_labels[i]]
            inter_df = inter_df[inter_df.Category == crime_labels[j]]
            sank_value.append(inter_df.size)
            
    #crime to resolution
    for i in range(len(crime_labels)):
        for j in range(len(resolution_labels)):
            
            #source and target
            sank_source.append(i + crime_offset)
            sank_target.append(j + resolution_offset)
            
            #value
            inter_df = ten_df[ten_df.Category == crime_labels[i]]
            inter_df = inter_df[inter_df.Resolution == resolution_labels[j]]
            sank_value.append(inter_df.size)
        
    return [sank_source,sank_target,sank_value]














