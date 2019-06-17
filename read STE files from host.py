#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 12:54:48 2019

@author: jack
"""

import urllib
import mechanize
import urllib.request, urllib.error


href = 'href='
aref = 'a href='
url = 'https://www.eternea.org/LookupSte.aspx?Sender=NDE'
tag='<td style="text-align:center;">'

SDE = 'http://www.eternea.org/LookupSte.aspx?Sender=SDE'
login = "http://www.eternea.org/login.aspx?ReturnURL=SteCats.aspx"
login = "http://www.eternea.org/Login.aspx"

init = "http://www.eternea.org"
uname = "capt_quixote@yahoo.com"
pword = "zzzz1234"
outpath = '/home/jack/DS/data/HTMLs/'
url = SDE


def get_outname(url):
    outname = outpath + url[-4:] + ".html"
    return(outname)
    
    
print("start:")
br = mechanize.Browser()
br.open(SDE)
br.select_form(nr=0)

br.form['ctl00$ContentPlaceHolder1$txtUserName'] = uname
br.form['ctl00$ContentPlaceHolder1$txtPassword'] = pword
req = br.submit()


url_list = []
outname = []

i=0
k=0
rejects=0

for link in br.links():
    save = link.url
    k=k+1
    url = 'http://www.eternea.org' 
    numb = save[-4:]
    if numb.isdigit() == True:
        url = url + save# +".html"
        url_list.append(url)
        outname = outpath + numb + ".html"
    else:
        outname = ""
        rejects=rejects+1
#        print("numb=",numb)
print("total=",k,"rejects=",rejects)


#print("\nlink:",link,"\nsave:",save,"\nurl:",url)
good_cnt = 1
for url in url_list:
    try:
        pr = mechanize.Browser()
        pr.open(url)
        pr.select_form(nr=0)

        pr.form['ctl00$ContentPlaceHolder1$txtUserName'] = uname
        pr.form['ctl00$ContentPlaceHolder1$txtPassword'] = pword
##        pr.form['ctl00_ContentPlaceHolder1_btnNextCase'] = '1012'
  #      http://www.eternea.org/ViewSte.aspx?CaseID=1012
        req = pr.submit()
        x = str(req.read())
        print("data_len = ",len(x))
        outname = get_outname(url)
        
        #fp = urllib.request.urlopen(url)
        #mybytes = fp.read()
        #mystr = mybytes.decode("utf8")
  #      x = mybytes.decode("utf8")
 #       fp.close()
        
        # save the file again
        with open(outname, "w") as outf:
            outf.write(str(x))

    except urllib.error.HTTPError as e:
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
            print('URLError: {}'.format(e.reason))
    else:# 200
        good_cnt = good_cnt + 1
        print('good ',good_cnt,outname)
