import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

db = json.load(open('datasets/usda_food/database.json'))
print(len(db))
print(db[0].keys())
print(db[0]['nutrients'][0])

nutrients = pd.DataFrame(db[0]['nutrients'])
print(nutrients[:7])

info_keys = ['description', 'group', 'id', 'manufacturer']
info = pd.DataFrame(db, columns=info_keys)
print(info[:5])
print(info.info())
print(info.group.value_counts()[:10])

print(nutrients)

# 有错