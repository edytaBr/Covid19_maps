#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 21:05:59 2020

@author: edyta
"""


# Import libraries
import pandas as pd
import folium
import os
import csv
import pandas as pd
from covid import Covid
import json
from countryinfo import CountryInfo

covid = Covid()
covid.get_data()




#Extract countries names from geojson
with open('europe.geojson') as data:
    geo = json.load(data)
    
    
countries = []
for item in geo['features']:
    countries.append(item['properties']['NAME'])
    
    
#Create dataset from worldmeters by using countries from geojson
list1 = []
for element in countries:
     list1.append((covid.get_status_by_country_name(element))['confirmed'])
    
    
data = {}
for keys in countries:
    for num in list1:
        data[keys] = num
        list1.remove(num)
        break
    


#Population and R rate for co
cases = []
for element in countries:
     cases.append((covid.get_status_by_country_name(element))['confirmed'])

countries = ['Azerbaijan', 'Albania', 'Armenia', 'Bosnia and Herzegovina', 'Bulgaria', 'Cyprus', 'Denmark',
           'Ireland', 'Estonia', 'Austria', 'Czech Republic', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 
           'Croatia', 'Hungary', 'Iceland', 'Israel', 'Italy', 'Latvia', 'Belarus', 'Lithuania', 'Slovakia', 'Liechtenstein', 
            'Malta', 'Belgium', 'Luxembourg', 'Monaco',  'Netherlands', 'Norway', 'Poland', 
           'Portugal', 'Romania', 'Moldova', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom', 'Ukraine', 'San Marino', 'Serbia', 'Russia']

##no macedonia, montenegro

population= []
for land in countries:
    population.append(CountryInfo(land).population())



data_cases = {}
for keys in countries:
    for num in cases:
        data_cases[keys] = num
        cases.remove(num)
        break


data_population = {}
for keys in countries:
    for pop in population:
        data_population[keys] = pop
        population.remove(pop)
        break


ratio = {}
for key in data_cases:
    for key1 in data_population:
        if key == key1:
            ratio[key] = (data_cases[key1]/ data_population[key])*100




#Change dictionary with data to csv file and save.     
df = pd.DataFrame(list(ratio.items()),columns = ['Country','Ratio'])
df.to_csv(r'/home/edyta/corona/korona_ratio.csv')
korona_ratio = os.path.join('/home/edyta/corona/', 'korona_ratio.csv')
korona_ratio = pd.read_csv(korona_ratio)


#Change dictionary with data to csv file and save.     
df = pd.DataFrame(list(data.items()),columns = ['Country','Cases'])
df.to_csv(r'/home/edyta/corona/korona.csv')
korona = os.path.join('/home/edyta/corona/', 'korona.csv')
korona = pd.read_csv(korona)


#Folium map
#europe = os.path.join('/home/edyta/corona/','europe.geojson')
m = folium.Map(location=[55, 10], zoom_start=4,  tiles='cartodbdark_matter')
#geojson_layer = folium.GeoJson(europe,name='geojson', show=False).add_to(m)

for item in geo['features']:
    for rat in korona_ratio['Ratio']:
        item['properties']['ratio'] = rat


m.choropleth(
 geo_data=geo,
 name='Corona',
 data=korona,
 columns=['Country', 'Cases'],
  key_on='properties.NAME',
 fill_color= 'Reds', fill_opacity=0.4, line_opacity=0.9, 
 threshold_scale=[50, 1000, 3000, 5000,15000, 50000,60000, 70000, 1000000]
)



m.choropleth(
 geo_data=geo,
 name='Corona_ratio',
 data=korona_ratio,
 columns=['Country', 'Ratio'],
  key_on='properties.NAME',
 fill_color='Reds', fill_opacity=0.4, line_opacity=0.9,
  threshold_scale=[0, 1,2, 620],
  show = False
)
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
NIL=folium.features.GeoJson(
        geo,
        style_function=style_function,
        control=False,
        highlight_function=highlight_function,
        tooltip=folium.features.GeoJsonTooltip(fields=['NAME', 'ratio'],
            aliases=['Name', 'R: '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
            sticky=True
        )
    )
m.add_child(NIL)

#Add popup
#geo_json = folium.GeoJson(geo, popup=folium.GeoJsonPopup(fields=['NAME']), show =False)
#geo_json.add_to(m)
#Save to .html
folium.LayerControl().add_to(m)

m.save('Corona.html')
