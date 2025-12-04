# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 22:09:15 2025

@author: Georg
"""

import xmltojson

with open(r'Aeldari - Aeldari Library', 'r') as f:
        my_xml = f.read()
xmltojson.parse(my_xml)