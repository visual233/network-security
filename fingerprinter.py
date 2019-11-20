# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:23:16 2019

@author: WXS
"""

import scapy.all as sc
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', help='pacp file')
args = parser.parse_args()

pks = sc.rdpcap(args.file)
x = 0
for p in pks:
    x += len(p['TCP'].payload)
    
dic = {'bing':0, 'canvas':0, 'craigslist':0, 'autolab':0, 'neverssl':0, 'tor':0, 'wikipedia':0}

df = pd.read_csv('info.csv')
X_train = np.array(df['length']).reshape(35,1)
Y_train = np.array(df['dist'])


model = KNeighborsClassifier(n_neighbors=4)
model.fit(X_train, Y_train)

y = model.predict_proba([[x]])

for k,p in zip(dic.keys(),y[0]):
    dic[k] = p
print(dic)

