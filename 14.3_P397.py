import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
names1880 = pd.read_csv('datasets/babynames/yob1880.txt', names=['name', 'sex', 'births'])
print(names1880)

print(names1880.groupby('sex')['births'].sum())

years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = 'datasets/babynames/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)
names = pd.concat(pieces, ignore_index=True)
print(names)

total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
# print(names.groupby(['year', 'sex'])['births'].sum().unstack()) 与前面等价
print(total_births.tail())

total_births.plot(title='Total births by sex and year')

def add_prop(group):
    group['prop'] = group.births / group.births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)
print(names)

print(names.groupby(['year', 'sex']).prop.sum())

def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]

grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
top1000.reset_index(inplace=True, drop=True)
print(top1000)

boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']

total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)
print(total_births.info())

subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(12, 10), grid=False, title='Number of births per year')

table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=
           range(1880, 2020, 10))

df = boys[boys.year == 2010]
print(df)

prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
print(prop_cumsum[:10])

print(prop_cumsum.values.searchsorted(0.5))

df = boys[boys.year == 1900]
in1900 = df.sort_values(by='prop', ascending=False).prop.cumsum()
print(in1900.values.searchsorted(0.5) + 1)

def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
print(diversity.head())

diversity.plot(title='Number of popular names in top 50%')
# plt.show()

get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)
print(table.head())
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
print(subtable.head())
print(subtable.sum())

letter_prop = subtable / subtable.sum()
print(letter_prop)

fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)
#plt.show()

letter_prop = table / table.sum()
dny_ts = letter_prop.loc[['d', 'n', 'y'], 'M'].T
print(dny_ts.head())

dny_ts.plot()
# plt.show()

all_names = pd.Series(top1000.name.unique())
lesley_like = all_names[all_names.str.lower().str.contains('lesl')]
print(lesley_like)

filtered = top1000[top1000.name.isin(lesley_like)]
print(filtered.groupby('name').births.sum())

table = filtered.pivot_table('births', index='year', columns='sex', aggfunc='sum')
table = table.div(table.sum(1), axis=0)
print(table.tail())

table.plot(style={'M': 'k-', 'F': 'k--'})
plt.show()