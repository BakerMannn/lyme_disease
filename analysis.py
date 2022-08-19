#########################################################
"""Import Packages"""
#Data Manipulation
import pandas as pd
import numpy as np

#Data Visualization
import plotly.express as px 

#Data Import
import requests
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
import json

#########################################################
"""Data Import"""
#Lyme Disease
df = pd.read_excel('data.xlsx')

#County Fips
url = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697'
tables = pd.read_html(url, match='data')
df_fips = tables[0]
df_fips.dropna(inplace=True)

full_states = []
for x in ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'FLORIDA', 'GEORGIA', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND', 'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE', 'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA', 'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON', 'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']:
    full_states.append(x.title())
    
abbrevs = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
df['Stname'].replace(full_states, abbrevs, inplace=True)

df['Ctyname'] = df['Ctyname'].str.replace(' County', '')

#########################################################
"""Data Join"""
df_joined = df.merge(df_fips, left_on=['Ctyname', 'Stname'], right_on=['Name', 'State'])

#########################################################
"""Data Manipulation"""
df_joined.drop(['STCODE', 'CTYCODE', 'Name', 'State'], axis=1, inplace=True)

#Rename Columns
columns = ['Cases2000', 'Cases2001', 'Cases2002', 'Cases2003', 'Cases2004', 'Cases2005', 'Cases2006', 'Cases2007', 'Cases2008', 'Cases2009', 'Cases2010', 'Cases2011', 'Cases2012', 'Cases2013', 'Cases2014', 'Cases2015', 'Cases2016', 'Cases2017', 'Cases2018', 'Cases2019']
columns_new = ['2000', '2001', '2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019']

df_joined.rename(columns=dict(zip(columns, columns_new)), inplace=True)

#Pivot
df_pivot = df_joined.melt(id_vars=['Ctyname', 'Stname', 'FIPS'], 
                          var_name='Year', 
                          value_name='Cases')
#########################################################
"""Plot"""
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig = px.choropleth_mapbox(df_pivot, 
                           geojson=counties, 
                           locations='FIPS', 
                           color='Cases',
                           animation_frame='Year',
                           animation_group='Ctyname',
                           color_continuous_scale="thermal",
                           range_color=(0, 100),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                          )
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
fig.show()
fig.write_html('lyme_dise.html')


