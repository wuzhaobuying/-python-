import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
import json
path = 'datasets/bitly_usagov/example.txt'
records = [json.loads(line) for line in open(path)]
frame = pd.DataFrame(records)
print(frame.info())
print(frame.describe())
print(frame['tz'][:10])
tz_counts = frame['tz'].value_counts()
print(tz_counts)

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
print(tz_counts[:10])

fig, axes = plt.subplots(2, 2)

axes[0, 0].barh(tz_counts[:10].index, tz_counts[:10].values)
# plt.show()
print(frame['a'][1])
print(frame['a'][50])
print(frame['a'][51][:1000])
results = pd.Series([x.split()[0] for x in frame.a.dropna()])
print(results[:5])
print(results.value_counts())

cframe = frame[frame.a.notnull()]
cframe['os'] = np.where(cframe['a'].str.contains("Windows"), 'Windows', 'Not Windows')
print(cframe['os'][:5])

by_tz_os = cframe.groupby(['tz', 'os'])
agg_counts = by_tz_os.size().unstack().fillna(0)
print(agg_counts[:10])

indexer = agg_counts.sum(1).argsort()
print(indexer[:10])

count_subset = agg_counts.take(indexer[-10:])
print(count_subset)

count_subset = count_subset.stack()
count_subset.name = 'total'
count_subset = count_subset.reset_index()
print(count_subset[:10])

# axes[0, 1].barh(x='total', y='tz', hue='os', data=count_subset, width=)

def norm_total(group):
    group['normed_total'] = group.total / group.total.sum()
    return group

results = count_subset.groupby('tz').apply(norm_total)
# axes[1, 1].barh(x='normed_total', y='tz', hue='os', data=results)
# plt.show()
g = count_subset.groupby('tz')
results2 = count_subset.total / g.total.transform('sum')
print(results2)