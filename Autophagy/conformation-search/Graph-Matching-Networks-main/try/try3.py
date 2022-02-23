# -*- coding: utf-8 -*-
# @Time : 2022/2/2 0002 22:05
# @Author : Bobby_Liukeling
# @File : try3.py
import pandas as pd
import numpy as np
import pdb

df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'b', 'b', 'a', 'a', 'e']})

df["grade"] = df["raw_grade"].astype("category")
df["grade"].cat.categories = ["very good", "good", "very bad"]
pdb.set_trace()
df["grade"] = df["grade"].cat.set_categories(["very bad", "bad", "medium", "good", "very good"])
