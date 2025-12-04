# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 13:12:11 2025

@author: Georg
"""
import os 
import requests
import xmltojson
import json
import pandas as pd

path = 'https://raw.githubusercontent.com/BSData/wh40k-10e/main/'

data = {'AE': path + "Aeldari%20-%20Aeldari%20Library.cat",
        'AM': path + "Imperium - Astra Militarum - Library.cat",
        'TAU': path + "T'au Empire.cat"}

musteringRules = pd.read_csv('CSVs/MusteringRules.csv')

def getFaction(faction):
    path = 'XMLs/{}.txt'.format(faction)
    if os.path.exists(path):
        with open(path, "r") as f:
            factionJSON = json.load(f)
            return factionJSON['catalogue']
        
def getMusteringRules(Detachment):
    detachmentRules = musteringRules[musteringRules['id'] == Detachment]
    return detachmentRules
    

for faction in data.keys():
   localFile = 'XMLs/{}.txt'.format(faction)
   if not os.path.exists(localFile):
    resp = requests.get(data[faction])
    my_json = xmltojson.parse(resp.text)
    with open(localFile, "w") as f:
        f.write(my_json)
        
        
            
