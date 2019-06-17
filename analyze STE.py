#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:32:07 2019

@author: jack
"""
import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)

"""
Transcript - direct print output to a file, in addition to terminal.

Usage:
    import transcript
    transcript.start('logfile.log')
    print("inside file")
    transcript.stop()
    print("outside file")
"""

import sys

class Transcript(object):

    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass

def start(filename):
    """Start transcript, appending print output to given filename"""
    sys.stdout = Transcript(filename)

def stop():
    """Stop transcript and return print functionality to normal"""
    sys.stdout.logfile.close()
    sys.stdout = sys.stdout.terminal

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

labels = ['','','','','','','']

colors = ['r','y','g','b','c','k','m']

fn="data"
start('graphs')
df = pd.read_csv(fn, usecols=new_lst)
#print( df.columns)
    
# changed relationships
col_list = ['relship change','mar stat prior', 'mar stat after', \
            'spirituality  prior','spirituality  after']

y = []
x = []

#PLOT relationship changes
i=0
skip_flag = False
for item in col_list:
    x=[]
    y=[]
    data = df[item].value_counts().to_dict()
    total = len(df)
    print('\n',item)
    for ans, count in data.items():
        pct = round(100*count/total,3)
        if count > 1:
            y.append(pct)
            x.append(ans)
            print('{:7s} {:3d}  {:7.2f}%'.format(ans, count, pct))#pct))
    
    plt.title(titles[i])    
    i=i+1
    plt.bar(x,y,label=labels[i],color=colors[i])
    plt.legend()
    if skip_flag == True:
        skip_flag=False
    else:
        plt.show()
        #print('{:7s} {:3d}  {:7.2f}%'.format(ans, count, pct))#pct))
        skip_flag=True
    
total = len(df)
light_words = ['spiri','relig']
dark_words = {'agnos','atheist'}
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
  
#x=["spiritual",",religious","agnostic","atheist"] 
#y=df[('pr light')]
#plt.title("Spritual or Religious Before and After STE")
#plt.bar(x,y)
#plt.show()
print('\nlight to dark: {:7.2f}%'.format(100*l_d/total)    )  
print('light to light:{:7.2f}%'.format(100*l_l/total)    )      
print('dark  to light:{:7.2f}%'.format(100*d_l/total)    )
print('dark  to dark :{:7.2f}%'.format(100*d_d/total)    )

print("\nLight after SDE:   {:7.2f}%".format(100*(l_l+d_l)/total))
print("Dark  after SDE:   {:7.2f}%".format(100*(l_d+d_d)/total))
spirit_chan = spirit_unch = 0
for index, row in df.iterrows():
    if row['spirituality  prior'] == row['spirituality  after']:
        spirit_unch = spirit_unch +1
    else:
        spirit_chan = spirit_chan+1

un = spirit_unch/(spirit_chan + spirit_unch)*100
chan = spirit_chan/(spirit_chan + spirit_unch)*100
print('\nSpirituality \nchanged:{:7.2f}%, unchanged: {:7.2f}%'.format(un,chan))
stop()
        