# -*- coding: UTF-8 -*-
import json
import sys
import traceback

if len(sys.argv)>2:
    try:   
        value_1 = json.loads(sys.argv[1])
        value_2 = json.loads(sys.argv[2])
        value_1_set = set(value_1)
        value_2_set = set(value_2)
        print(value_1_set.issubset(value_2_set))
    except:
        traceback.print_exc()