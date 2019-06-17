#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:32:07 2019

@author: jack
"""
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)

all_lst = ['Unnamed: 0', 'type', 'case', 'age', 'coma', 'race', 'gender',
       'heritage', 'c’ship', 'comm sz', 'spirituality  prior',
       'spirituality  after', 'religion prior', 'religion after',
       'comments prior', 'comm after', 'rel lit', 'rel service',
       'strength rel conv', 'rel influ', 'income', 'educ', 'occp prior',
       'occp after', 'mar stat prior', 'mar stat after', 'relship change',
       'dr care']

new_lst = ['spirituality  prior','spirituality  after', 'religion prior', \
           'religion after','rel lit', 'rel service','strength rel conv', \
           'rel influ','mar stat prior', 'mar stat after', 'relship change']

titles = ["% of Relationships Changed", "% Marital Status1", \
          "% Marital Status2","Spirituality1","Spirituality2","4","5","6"]

labels = ['','prior','after','','','','']

colors = ['r','y','g','b','c','k','m']

fn="data"
df = pd.read_csv(fn, usecols=new_lst)
#print( df.columns)
    
# changed relationships
col_list = ['relship change','mar stat prior', 'mar stat after', \
            'spirituality  prior','spirituality  after']

#PLOT relationship changes
i=0

x=[]
y=[]
total = len(df)
data = df['relship change'].value_counts().to_dict()
for ans, count in data.items():
    pct = round(100*count/total,3)
    if count > 1:
        y.append(pct)
        x.append(ans)
#        print('{:7s} {:3d}  {:7.2f}%'.format(ans, count, pct))#pct))
plt.title("Did Relationships Change?")
plt.bar(x,y,label=labels[i],color=colors[i])
plt.show()

# MARRIAGE STATUS
x=[]
y=[]

data = df['mar stat prior'].value_counts().to_dict()
for ans, count in data.items():
    pct = round(100*count/total,3)
    if count > 1:
        y.append(pct)
        x.append(ans)
#        print('{:7s} {:3d}  {:7.2f}%'.format(ans, count, pct))#pct))

ind = np.arange(len(x))    
width = 0.35
plt.title("Marital Status %")
plt.bar(ind,y,width,color=colors[2],label="Before")
x=[]
y=[]
data = df['mar stat after'].value_counts().to_dict()
for ans, count in data.items():
    pct = round(100*count/total,3)
    if count > 1:
        y.append(pct)
        x.append(ans)
#        print('{:7s} {:3d}  {:7.2f}%'.format(ans, count, pct))#pct))
plt.bar(ind+width,y,width,color=colors[3],label="After")
plt.xticks(ind + width / 2, x)
plt.legend(loc='best')
plt.show()

#SPIRITUALITY
plt.title("% Spiritual/Religious v. Non")
x=[]
y=[]
data = df['spirituality  prior'].value_counts().to_dict()
for ans, count in data.items():
    pct = round(100*count/total,3)
    if count > 1:
        y.append(pct)
        x.append(ans)
#        print('{:7s} {:3d}  {:7.2f}%'.format(ans, count, pct))#pct))
ind = np.arange(len(x) )    
width = 0.35
plt.bar(ind,y,width,color=colors[4],label="Before")


x=[]
y=[]
data = df['spirituality  after'].value_counts().to_dict()
for ans, count in data.items():
    pct = round(100*count/total,3)
    if count > 1:
        y.append(pct)
        x.append(ans)
#        print('{:7s} {:3d}  {:7.2f}%'.format(ans, count, pct))#pct))
 
ind = np.arange(len(x))
plt.bar(ind+width,y,width,color=colors[5],label="After")
plt.xticks(ind + width / 2, x)
plt.legend(loc='best')
plt.show()
 
total = len(df)
#
df['pr light'] = 0
df['pr dark'] = 0
df['after light'] = 0
df['after dark'] = 0

l_d=0
l_l=0
d_l=0
d_d=0
 
for i, row in df.iterrows():
    df.at[i, 'pr light']  = int(('spiri' in row['spirituality  prior']) or \
         ('relig' in row['spirituality  prior']))
    df.at[i, 'pr dark'] =  int(('agnos' in row['spirituality  prior']) or \
         ('athe' in row['spirituality  prior']))
    
    df.at[i, 'after light']  = int(('spiri' in row['spirituality  after']) or \
         ('relig' in row['spirituality  after']))
    df.at[i, 'after dark'] =  int(('agnos' in row['spirituality  after']) or \
         ('athe' in row['spirituality  after']))

for i, row in df.iterrows():
    if row['pr light'] and row['after light']:
        l_l=l_l+1
    if row['pr light'] and row['after dark']:
        l_d=l_d+1
        
    if row['pr dark'] and row['after light']:
        d_l=d_l+1
    if row['pr dark'] and row['after dark']:
        d_d=d_d+1
  
    
plt.title("Perspective Changed")
light_after = (100*(l_l+d_l)/total)
dark_after = (100*(l_d+d_d)/total)
labels = 'Light to Dark', 'Light to Light','Dark to Light', 'Dark to Dark'
sizes = [l_d,l_l,d_l,d_d]
colors = ['lightcoral', 'lightskyblue', 'gold','green']
plt.pie(sizes, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.show()      

plt.title("Found God, or Not, after the NDE")
light_after = (100*(l_l+d_l)/total)
dark_after = (100*(l_d+d_d)/total)
labels = 'Found After', 'Not Found After'
sizes = [light_after, dark_after]
colors = ['lightcoral', 'lightskyblue']
plt.pie(sizes, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.show()      
        
#print("\nLight after SDE:   {:7.2f}%".format(100*(l_l+d_l)/total))
#print("Dark  after SDE:   {:7.2f}%".format(100*(l_d+d_d)/total))
spirit_chan = spirit_unch = 0
for index, row in df.iterrows():
    if row['spirituality  prior'] == row['spirituality  after']:
        spirit_unch = spirit_unch +1
    else:
        spirit_chan = spirit_chan+1

un = spirit_unch/(spirit_chan + spirit_unch)*100
chan = spirit_chan/(spirit_chan + spirit_unch)*100
labels = 'Changed', 'Unchanged'
sizes = [chan,un]
colors = ['gold', 'yellowgreen']
plt.title("Spirituality after the NDE")
plt.pie(sizes, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.show()
#print('\n\t\tSpirituality \nchanged:{:7.2f}%, unchanged: {:7.2f}%'.format(un,chan))
