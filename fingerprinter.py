# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:23:16 2019

@author: WXS
"""

import scapy.all as sc
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

pks = sc.rdpcap('pcaps/ssl/tor-ssl5.pcap')
x = 0
for p in pks:
    x += len(p['TCP'].payload)
    
print(x)

df = pd.read_csv('info.csv')
X_train = np.array(df['length']).reshape(35,1)
Y_train = np.array(df['dist'])


model = KNeighborsClassifier(n_neighbors=4)
model.fit(X_train, Y_train)

y = model.predict([[x]])
print(y)
