#!/usr/bin/python
"""
Created on Wed May  1 12:29:07 2019
@author: jack
"""
import pandas as pd
import os
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)

path = '/home/jack/DS/data/HTMLs/'

Qtag = '<td style="text-align:left; color:black;">'
Qtag = "Q-"
Qtag_len = len(Qtag)
Atag     = '<td style="text-align:left; color:blue;">'
Atag = "A-"
Atag_len = len(Atag)

Skip_tag = '<td style="text-align:left; color:blue;">'
skip_len = len(Skip_tag)

data_start = "Case ID:"

RBLACK= '<td style="text-align:right; color:black;">'
LBLACK = '<td style="text-align:left; color:black;">'
RBLUE = '<td style="text-align:right; color:blue;">'
LBLUE = '<td style="text-align:left; color:blue;">'

Atag_len = len(Atag)

ANS_LEN = 30
Q_LEN = 30

FIND_TYPE = "STE Type:"
BOF = '; \">'
TYPE=0
CASE=1
AGE=2
COMA=3
RACE=4
GENDER=4
DETAIL=GENDER+1

row=0

def bld_ques_df(df, q_df):
    for index, each in q_df.iterrows():
        df[each['col name']] = None
        
def build_q_lst(fn,q_lst):#build list of questions from file
    #print("build_list_of_ques")
    q_df = pd.read_csv(fn)  #build questions dataframe
    Q_CNT = 0
    for index, each in q_df.iterrows():
        q=each['question']
        q_lst.append(q)
        Q_CNT = Q_CNT +1

def get_age(data):
    x=q_df.iloc[AGE]['question']
    start_pos = data.find(x)#"Age at Event:")
    if( start_pos < 1):
        age=""
    else:
        start_pos = start_pos + len(LBLUE)+16
        end = start_pos+2 #+ 10
        age  = int(data[start_pos:end])
    return(age)
    
def get_case(data):
    x=q_df.iloc[CASE]['question']
    case = "xxx"
    start_pos = data.find(x)
    if start_pos > 1:
        start_pos = start_pos + len(x) +4
        end = start_pos + 4
        case  = data[start_pos:end]
        if ( int(case) < 1000):
#            print("case:",case)
            start_pos = start_pos + 4
            end = start_pos+4 
            case  = data[start_pos:end]            
    return(case)
    
def get_gender(data):
    start_pos = data.find("Female")
    if start_pos > 1:
        return("F")
    
    start_pos = data.find("Male")
    if start_pos > 1:
        return("M")
    return("")
    
def get_race(data):
    x=q_df.iloc[RACE]['question']
    start_pos = data.find(x) +len(x)+len(Atag)+9
    if start_pos > 1:
        end = start_pos+15
        r = data[start_pos:end]
        r = r.replace("\\n", "")
        r = r.replace("A-", "")
    return(r)
  
def clean_data(data):
    data = data.replace("\n", "")
    data = data.replace(RBLACK, "")
    data = data.replace(LBLACK, Qtag)
    data = data.replace(RBLUE, "")
    data = data.replace(LBLUE, Atag)
    data = data.replace("\\r\\n\\t"," ")
    data = data.replace("\\r\\n"," ")
    data = data.replace("</td>", " ")
    data = data.replace("</tr>", " ")
    data = data.replace("<tr>", " ")
    data = data.replace("\\t", " ")
    data = data.replace("\t", " ")
    data = data.replace("  ", " ")
    data = data.replace("A.	\\n", "A.")
    data = data.replace(" -","")
    data = data.replace("&#39;","")
    data = data.replace("&quot;","")
    data = data.replace("_","")
    return(data)
  
def get_detail(data):
    data_ptr = data
    start = data_ptr.find("Please describe your STE in detail.")
    if ( start > 0):
        data_ptr = data[start:5000+start]
        end = data_ptr.find(Qtag)-len(Qtag)-2
        start = data_ptr.find(Atag)+Atag_len
        data_ptr = data_ptr[start:end]
        return(data_ptr)
    else:
        return("")
        
        
"""       START HERE
"""
start_time = time.time()
print("Start")

df = pd.DataFrame()

questions_filename = "questions.csv"
q_df = pd.read_csv(questions_filename)
bld_ques_df(df, q_df)

empty = [None] * len(df.columns)

# build dir name
files = []
for r, d, f in os.walk(path): # r=root, d=directories, f = files
    if f == '1':
        print("1")
    else:
        for file in f:
            if '.html' in file:
                files.append(os.path.join(path, file))

file_cntr=0
for fn in files:
    try:
        file = open(fn,mode='r')
        #print("Opened:",fn)
    except:
        print ("failed open :",fn)
      
    file_cntr = file_cntr+1
    if( file_cntr % 100 == 0):
        x="processing..." + str(file_cntr)
        print("\r {}".format(x), end="")
        
    row = len(df)
    df.loc[row] = empty
    
    file_data = file.read() 
    file_data = clean_data(file_data)
    start = file_data.find(data_start)
    
    start = file_data.find(FIND_TYPE)  #finde label
    temp_ptr = file_data[start:]           # move to label
    start = temp_ptr.find(BOF)  # find data field marker
    start = start + 4
    end = start + 3
    df.iloc[row][TYPE] = temp_ptr[start:end]
    df.iloc[row][CASE] = get_case(file_data)
    df.iloc[row][AGE] = get_age(file_data)
    df.iloc[row][RACE] = get_race(file_data)
    df.iloc[row][GENDER] = get_gender(file_data)
    data_ptr = get_detail(file_data)
    df.iloc[row][DETAIL] = data_ptr

    for index,ques in q_df.iloc[7:].iterrows(): #skip category answers
        fld_len = q_df.iloc[index]['fld len']
        question = ques['question']
        q_ptr = file_data.find(question)
        data = file_data[q_ptr:q_ptr+100]
        a_ptr = data.find(Atag)
        data = file_data[q_ptr:q_ptr+100]
        a_ptr = data.find(Atag)
        answer=  data[a_ptr:a_ptr+fld_len+3]   
        answer = answer.replace("A-\\n","")
        answer = answer.replace(" -","")
        answer = answer.rstrip()
        answer = answer.replace("A-","")
        col_name = q_df.iloc[index]['col name']
        df.iloc[row][col_name] = answer#get_religion(data)
  
    
bins= [-1,21,60,100]
labels = ['youth','adult','senior']
df['agegroup'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

for index, row in df.iterrows():
    brand = df.iloc[index]['rel prior']
    if brand.find("Christi") > -1:
        df.at[index,'rel prior'] = 'Christian'
    if brand.find("Unit") > -1:
        df.at[index,'rel prior'] = 'Unity'   
        
    brand = df.iloc[index]['rel after']
    if brand.find("Christi") > -1:
        df.at[index,'rel after'] = 'Christian'
    if brand.find("Unit") > -1:
        df.at[index,'rel after'] = 'Unity'
        
    lit =  df.iloc[index]['rel lit']
    if lit.find("week") > -1:
        df.at[index,'rel lit'] = 'weekly'
        
    conv =  df.iloc[index]['strength rel conv']
    if conv.find('very') > -1:
        df.at[index,'strength rel conv'] = 'very strong'
        
    rel_serv =  df.iloc[index]['rel service']
    if rel_serv.find('seld') > -1:
        df.at[index,'rel service'] = 'seldom'
        
    cs =  df.iloc[index]['conv strength']
    if cs.find('none') > -1:
        df.at[index,'conv strength'] = 'none'
        
    brand = df.iloc[index]['content of NDE']
    if brand.find("Both pleasant and") > -1:
        df.at[index,'content of NDE'] = 'Pleasant&distressing'
    if brand.find("Entirely distressing") > -1:
        df.at[index,'content of NDE'] = 'All distressing'
    if brand.find("Neither plesant nor") > -1:
        df.at[index,'content of NDE'] = 'Not pleasnt nor distressing'
    if brand.find("Entirely pleasant") > -1:
        df.at[index,'content of NDE'] = 'All pleasant'
        
"""  analyze
"""
fn = "data"
df.to_csv(fn)
print("\nseconds:", round((time.time() - start_time),2))