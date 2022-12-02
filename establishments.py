# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 19:51:09 2022

@author: Sasha
"""

import pandas as pd
import numpy as np
import math 
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stat
import sidetable as stb
import streamlit as st
import altair as alt
from PIL import Image
import pandas_usaddress as pu
st.write('''
         # How to tell a story using data - project
         ''')
st.write('''
         ### In the coming project we are going to investigate data of different types of \
            restauraunts across LA.Our willing is to invest in small robot-run cafe, \
            wich is promising but expensive. In order to increase our chanses to sucsseed \
            in this project we will try to understand what is the optimal restraunt type \
            we should invest in, what are the optimal spots for this kind of restraunts \
            and how big should it be ( in terms of capacity).After our first step of \
            reading and prepearing the data to provide reliability we will investegate the \
            more and the less sucssessive restaurants due to their types, locations and \
            capacity and we'll try to provide the options that most suits our project. We \
            will compare chains to single restraunts, what types of retaurants got the \
            bigger potential for development and wether it worth it. We will check the \
            share of market for each type of restaurant and provide distribution of the \
            capacity via locations and via types,and of course much more exciting info and\
            graphs will be provided in the upcoming project! 
         ''') 
image = Image.open('C:/Users/Sasha/.streamlit/Tell_A_Story_With_Data_Blog_Header.png')
st.image(image)
st.write('''
         ## In the first step of the project we'll read the data and prepare it for\
         analysis by checkig missing values, types duplicates and overall visuality\
         of the data frame and wether it's reliable or we should change/fix something. 
         ''')      
st.subheader('''
         short table of the provided data after fixing: 
         ''') 
df = pd.read_csv( r'C:\Users\Sasha\Desktop\practicum100\8. How to tell a story using data - Streamlit\project\rest_data_us.csv')
df.columns = ['id','object_name','address','chain','object_type','seats']
st.table(df.head()) 
#st.write("""
#         #### After changing the name of the number column to seats, so it'll be more
#         clear, we'll convert the objects to lowercase for similarity and the "object_type"
#         column to category type for memory efficiency
#         """)
df['object_name'] = df['object_name'].str.lower() 
df['address'] = df['address'].str.lower()
df['object_type'] = df['object_type'].str.lower()
df['object_type'] = df['object_type'].astype('category')
#st.write('''
#         ### proportions of the various types of establishments
#         ''')
type_prop = df.groupby('object_type',as_index=False)['id'].count()
type_prop.columns = ['object_type', 'facilities']
#st.table(type_prop.sort_values('facilities', ascending = False))
prop_est_fig = px.pie(
    type_prop, values='facilities', names='object_type')#, title = 'Proportions of the various types of establishments')
prop_est_fig.update_layout(
title = 'Proportions of the various types of establishments')
st.subheader('''
         A table with the amount of facilities for each type of establishment : 
         ''') 
st.dataframe(type_prop)
#st.write('A table with the amount of facilities for each type of establishment :', type_prop)
st.plotly_chart(prop_est_fig)
'*The beyond pie chart illustrates us the huge proportion of the restaurants (more than \
  75%) from the various types of establishments. The fast food is second with 11%, after \
  comes the coffe establishments with 4.5%, while all 3 others got more or less the same share of 3%.'
st.subheader('''
         A chain vs not a chain: 
         ''')
chain_df = df.groupby('chain')['id'].count().reset_index()
chain_df.columns = ['chain','amount']
chain_df['chain'] = chain_df['chain'].apply(lambda x: "A chain" if x == True else "Not a chain")
chain_prop = plt.figure(figsize=(8,6))
plt.bar(chain_df['chain'], chain_df['amount']);
st.pyplot(chain_prop)
'*It turns to be there are  more non-chain establishments than chains.'
typically_prop = df.groupby(['object_type','chain'])['id'].count().reset_index()
typically_prop.columns = ('object_type','chain','facilities')
chain_typically_prop =  typically_prop[typically_prop['chain']==True]
not_chain_typically_prop =  typically_prop[typically_prop['chain']==False]
est_is_chain = alt.Chart(typically_prop).mark_bar().encode(
x = alt.X('sum(facilities)', stack='normalize', title = 'chains/non-chains percentage'),
y = 'object_type',
color='chain').properties(
    width=600,
    height=300)
#est_is_chain
st.subheader('Type of establishments that are  typically a chain:')
st.altair_chart(est_is_chain)
'*When sorting by types of establishments we discover that even though most of the overall\
establishments are not a chain with some gap, most of the establishments individually are\
actually chains. Moreover, the Bakery industry got only chains!!<br> Fast foods and cafes\
got more chains than not chains establishments, while pizzas are somewhere in the middle\
with very slightly advantage that is almost unnoticed. Only resturants and bars got more\
chain facilities indeed.'
st.subheader('A Scatterplot regarding the characteristics of chains by the amount of \
             establishments and the number of seats:')
chains_df = df[df['chain'] == True]
not_chains_df = df[df['chain'] == False]
chains_char = chains_df.groupby('object_name', as_index = False).agg({'seats':'mean','id':'count'})
chains_char.columns = ['object_name','average_seats','establishments']
chains_char_graph = alt.Chart(chains_char).mark_circle(size=70).encode(
x = 'average_seats',
y = 'establishments',
tooltip = ['object_name','average_seats','establishments']).properties(
    width=800,
    height=450
).interactive()
chains_char_graph
'* Analyzing the scatterplot regarding the characteristics of chains we can see clearly \
   that mostly there are not many establishments in LA when it comes to chains, mostly \
   only one. Probably the others are not in LA. As for the  chains seats, half of the \
   chains establishments got 26 seats and more.<br> Visualizing the graph we can say that\
   there are more  few establishments with a lot of seats than many establishments with a\
   small number of seats.'
seats_by_types = df.groupby('object_type',as_index = False).agg({'seats':'mean'}).round()
st.subheader('A table of average number of seats for each type of establishment:')
st.dataframe(seats_by_types)
avg_seats_by_type = alt.Chart(seats_by_types).mark_bar().encode(
x = 'object_type',
y = 'seats',
color = 'object_type').properties(width = 500, height = 600)
st.altair_chart(avg_seats_by_type)
' * As we could probably predict, restaurant have the largest number of seats, while bars \
  are not far behind. The lowest number of seats is in bakerys, wich make sense as well.'
df = pu.tag(df,['address'], granularity='medium', standardize=True)
fillna_list = ['StreetNamePreDirectional','StreetName','StreetNameSuffix']
for col in fillna_list:
    df[col] = df[col].fillna('')

df['street'] = df['StreetNamePreDirectional']+ ' ' + df['StreetName'] + ' ' + df['StreetNameSuffix']

df = df.drop(fillna_list, axis=1)

for i in range(len(df)):
    if df['PlaceName'][i] == 'olvera':
        print(df['id'][i])
        df['street'][i] = df['PlaceName'][i] + ' ' + df['StateName'][i]
    elif df['StreetNamePrefix'][i] == 'wilshire':
        print('wilshire',df['id'][i])
        df['street'][i] = df['StreetNamePrefix'][i]
    elif df['PlaceName'][i] == 'santa':
        print('santa fe',df['id'][i])
        df['street'][i] =  df['StreetNamePostDirectional'][i] + ' ' + df['PlaceName'][i] + ' ' + df['StateName'][i] 

nan_df = df[df['street'] == '  '].reset_index()

id_list = []
astronaut_list =[]
cesar_list =[]
for i in range(len(nan_df)):
    if (nan_df['address'][i]).split()[3] == 'slater':
        slater_id = nan_df['id'][i]
        slater = 's slater st'
        id_list.append(slater_id)
    elif (nan_df['address'][i]).split()[2] == '1st':
        first_id = nan_df['id'][i]
        first = '1st st'
        id_list.append(first_id)
    elif (nan_df['address'][i]).split()[2] == '6th':
        sixth_id = nan_df['id'][i]
        sixth = '6th st'
        id_list.append(sixth_id)
    elif (nan_df['address'][i]).split()[3] == 'figueroa':
        figueroa_id = nan_df['id'][i]
        figueroa = 's figueroa st'
        id_list.append(figueroa_id)
    elif (nan_df['address'][i]).split()[3] == 'avenue':
        avenue_id = nan_df['id'][i]
        avenue = 's grand avenue low plaza'
        id_list.append(avenue_id)
    elif (nan_df['address'][i]).split()[3] == 'central':
        central_id = nan_df['id'][i]
        central = 's central ave'
        id_list.append(central_id)
    elif (nan_df['address'][i]).split()[2] == 'cesar':
        cesar_id = nan_df['id'][i]
        cesar = 'w cesar e chavez ave'
        cesar_list.append(cesar_id)       
    elif (nan_df['address'][i]).split()[1] == 'astronaut':
        astronaut_id = nan_df['id'][i]
        astronaut = 'astronaut e. s. onizuka st'
        astronaut_list.append(astronaut_id)
        
for i in range(len(df)):
    if df['id'][i] == slater_id:
        df['street'][i] = slater
    elif df['id'][i] == first_id:
        df['street'][i] = first
    elif df['id'][i] == sixth_id:
        df['street'][i] = sixth
    elif df['id'][i] == figueroa_id:
        df['street'][i] = figueroa
    elif df['id'][i] == avenue_id:
        df['street'][i] = avenue   
    elif df['id'][i] == central_id:
        df['street'][i] = central  
    elif df['id'][i] == central_id:
        df['street'][i] = central
    elif df['id'][i] in (cesar_list):
        df['street'][i] = cesar
    elif df['id'][i] in (astronaut_list):
        df['street'][i] = astronaut
        
df['street'] = df['street'].apply(lambda x: ((x.split(' ', 1)[1]).lstrip()) if x.split()[0] == '12' or x.split()[0] == '14' or \
                                  x.split()[0] == '34' else x)

df['street'] = df['street'].apply(lambda x: x.lstrip())       
        
for i in range(len(df['street'])):
    if df['id'][i] == 20492:
        df['street'][i] = 's san pedro st'
    elif df['id'][i] == 13320:
        df['street'][i] = 's san pedro st'
    elif df['id'][i] == 14618:
        df['street'][i] = 'n san fernando rd'   
        
df['street'] = df['street'].apply(lambda x: x.rstrip())

for i in range(len(df['street'])):
    if df['street'][i] == 'e cesar':
        df['street'][i] = 'e cesar e chavez'
    elif df['street'][i] == 'astronaut':
        df['street'][i] = 'e astronaut e s onizuka st'
    elif df['street'][i] == 'w 6th':
        df['street'][i] = 'w 6th st'
    elif df['street'][i] == 'e charles':
        df['street'][i] = 'e charles e young dr'  
    elif df['street'][i] == 's charles':
        df['street'][i] = 's charles e young dr'

df = df.drop('PlaceName', axis=1)  
df = df.drop('USPSBox', axis=1)      

for i in range(len(df)):
    if df['street'][i] == 'e astronaut':
        print(df['street'][i])
        df['street'][i] = 'e astronaut e s onizuka st'

df = df.drop('ZipCode', axis =1)       
df = df.drop('StateName', axis =1) 

for i in range(len(df)):
    if df['id'][i] == 11924:
        df['street'][i] = df['StreetNamePrefix'][i]
    elif df['id'][i] == 11939:
        df['street'][i] = 'e 7th st'
    elif df['address'][i].split()[1] == 'n' and df['address'][i].split()[2] == 'avenue':
         df['street'][i] = 'n avenue'
    elif df['address'][i].split()[1] == 's' and df['address'][i].split()[2] == 'avenue':
         df['street'][i] = 's avenue'
    elif df['address'][i].split()[1] == 'w' and df['address'][i].split()[2] == 'avenue':
         df['street'][i] = 'w avenue'
    elif df['id'][i] == 13133:
        df['street'][i] = 'w 3rd st'
    elif df['id'][i] == 13163:
        df['street'][i] = 'e 7th pl'
    elif df['id'][i] == 13390:
        df['street'][i] = 'e century park' 
    elif df['id'][i] == 13893:
        df['street'][i] = 'e 1st st' 
    elif df['address'][i].split()[1] == 'avenue' and df['address'][i].split()[4] == 'stars':
         df['street'][i] = 'avenue of the stars'
    elif df['address'][i].split()[1] == 'ave' and df['address'][i].split()[3] == 'stars':
         df['street'][i] = 'avenue of the stars'
         
for i in range(len(df)):
    if df['address'][i].split()[1] == 'world' and df['address'][i].split()[2] == 'way':
        df['street'][i] = 'world way'
    elif df['address'][i].split()[1] == 'e' and df['address'][i].split()[2] == '12th':
        df['street'][i] = 'e 12th st'
    elif df['address'][i].split()[1] == 'e' and df['address'][i].split()[2] == '1st':
        df['street'][i] = 'e 1st st'
    elif df['address'][i].split()[1] == 'e' and df['address'][i].split()[2] == '8th':
        df['street'][i] = 'e 8th st'
    elif df['address'][i].split()[1] == 'e' and df['address'][i].split()[2] == '9th':
        df['street'][i] = 'e 9th st'
        
for i in range(len(df)):
    if df['id'][i] == 18888:
        df['street'][i] = 'w imperial hwy'
    elif df['id'][i] == 19744:
        df['street'][i] = 'california state route'
    elif df['address'][i].split()[1] == 'e' and df['address'][i].split()[2] == '7th':
        df['street'][i] = 'e 7th st'
    elif df['id'][i] == 21358:
        df['street'][i] = 's spring'
df = df.drop('StreetNamePrefix', axis =1)
df = df.drop('StreetNamePostDirectional', axis =1)
df = df.drop(['AddressNumber', 'OccupancySuite'], axis =1)

st.subheader('A table of top ten streets by number of restaurants.:')

streets_by_restaurant = df.groupby('street')['id'].count().reset_index()
streets_by_restaurant.columns = ['street','restaurants']
top_ten = streets_by_restaurant.sort_values('restaurants',ascending=False).head(10)
st.dataframe(top_ten)

st.subheader('Bar chart with top ten streets having most of restaurants:')
top_ten_bar = alt.Chart(top_ten).mark_bar().encode(
x = 'street',
y = 'restaurants').properties(width = 500, height = 600)

st.altair_chart(top_ten_bar)

'* The street with the most restaurants is  wilshire blvd followed by w sunset blvd and \
   w pico blvd, when they all have more than 300 restaurants, the other streets in the top\
       10 got 200s of them.'

'!! There are: ',len(streets_by_restaurant[streets_by_restaurant['restaurants'] == 1]),\
                          ' streets having only one restaurant from our data.'
                          
top_ten_distr = df[df['street'].isin(top_ten['street'])]

st.subheader('The distribution of the number of seats for top streets:')

top_ten_distr_boxplot = plt.figure(figsize=(16,12))
sns.boxplot(x='street',y='seats',data=top_ten_distr);

top_ten_distr_boxplot
'* The distribution of the seats in the establishments of top streets are leaded by wilshere\
 blvd and hollywood blved with the biggest averages, while all of the streets have a lot \
 of outliers with large amount of seats, only the s western blvd and w 3rd street do not \
 really have restaurants with more than 200 seats.'

top_restaurants = top_ten_distr[top_ten_distr['object_type'] == 'restaurant']
top_restaurants_grouped = top_restaurants.groupby('street', as_index=False).agg({'id':'count','seats':'mean'})
top_restaurants_grouped.columns = ['street','restaurants','seats']
top_restaurants_grouped['seats'] = top_restaurants_grouped['seats'].round()

most_restaurants = alt.Chart(top_restaurants_grouped).mark_bar().encode(
x = 'street',
y = 'restaurants').properties(width = 500, height = 600)

st.subheader('Streets with most establishments of restaurant type')

st.altair_chart(most_restaurants)

'* Wilshere blvd still top of the table, even when checking only restaurants.'

st.subheader('Streets with most capacity of restaurant type')

most_seats = alt.Chart(top_restaurants_grouped).mark_bar().encode(
x = 'street',
y = 'seats').properties(width = 500, height = 600)

st.altair_chart(most_seats)

'* When it comes to avg. capacity the hollywood blvd is the best option, whie wilshere \
    blvd comes after. Sunset blvd and w olympic blvd are slightly behind.'
    

st.subheader('Distribution of capacity among the top streets - restaurant type only')    
    
most_restaurants_boxplot = plt.figure(figsize=(15,12))
sns.boxplot(x='street',y='seats',data=top_restaurants);   

most_restaurants_boxplot 

'* The distribution of the sunset blvd and the hollywood blvd look even a bit more solid\
    than wilshere blvd in the boxplots above where we check only restaurants. '

st.write('''
         ## Overall conclusion:
         ''')
st.write('''
         When we first look at the proportions of the various types of establishments, it \
         seems obvious to invest in the restaurants, since they occupie more than 75% of \
         the market and it seems reasonable to get into this sphere.But when we realize that \
         most of the establishments aren't chains we should have second thoughts, since if \
         we want our bussiness to develop and become a chain, we should probably prioritize\
         the types of restaurants that have more potential to develop. The graph that shows\
         the type of establishments that are typically a chain illustrates us that most of\
         the restaurants are't chains, while all of the bakerys are, but does a bakery\
         suits our willing? Suposely we would like to invest in more luxury establishment \
         due to the fact that our project is expensive, but we should explore all our options.\
         Caffes, fast food and pizzas establishments have a bigger potential to become a chain\
         as well.The scatterplot of the characteristics of chains reduces a bit the desire\
         to evolve and become a chain, since most of the chains are small and even considering\
         the fact that it's a progress, it isn't as big as we would probably wish, and becoming \
         a big chain seems very chalenging, so maybe the restaurant type of establishment\
         can suit us after all. Looking at the graph that produce the average number of \
         seats in different type of establishments, we announce the restaurant as the winner\
         , while bars are not far behind. It streghtens the odds of choosing a restaurant\
         type of facility for our business, because the more seats we have, the potential of our\
         revanue grows accordingly.After discussing the type of establishment we should invest\
         in for our bussiness we have to check for the best location for it. We should \
         probably pick the streets with the most establishments since our planned bussiness \
         is going to be unique and we should apperantly beat our competitors. The Bar chart\
         with top ten streets having most of restaurants leaves us with 3 main options wich \
         are: wilshire blvd,sunset blvd and w pico blvd that have some advantage over the\
         others. The distribution of the number of seats for top streets illustrates the \
         adventage of wilshere blvd over the others, while the closest competitor here is \
         surprisengly the hollywood blvd having probably even slightly better distribution,\
         especially when checking restaurants only. The restaurants only distribution boxplots\
         graph brings in a new serious contender - the sunset blvd, with even better distribution\
         than the two discussed above, and holding the second place in the graph of the number\
         of restaurants. Bottom, after taking into account our whole project, we would suggest\
         invest in establishment type of restaurant in the sunset blvd or in wilshere blvd!!'
         ''')