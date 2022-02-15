# -*- coding: UTF-8 -*-
import json
import sys

if len(sys.argv)>2:   
    value_1 = json.loads(sys.argv[1])
    value_2 = json.loads(sys.argv[2]) 
    value_1_set = value_1.keys()
    value_2_set = value_2.keys()
    print(value_1_set = value_2_set)