# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 16:01:23 2019

@author: WXS
"""

import os
import scapy.all as sc
import pandas as pd

dirs = os.listdir('pcaps')
dic = {'bing': 1, 'canvas': 2, 'dc': 3, 'grader': 4, 'ssl': 5, 'tor': 6, 'wiki':7}
data = {'dist': [], 'length': []}
for d in dirs:
    p1 = os.path.abspath('pcaps')
    p1 = os.path.join('pcaps',d)
    files = os.listdir(p1)
    for f in files:
        l = 0
        p2 = os.path.join(p1,f)
        pks = sc.rdpcap(p2)
        for p in pks:
            l += len(p['TCP'].payload)
        data['dist'].append(dic[d])
        data['length'].append(l)
        
df = pd.DataFrame(data)
df.to_csv('info.csv')
        