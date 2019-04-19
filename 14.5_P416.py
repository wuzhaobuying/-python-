import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fec = pd.read_csv('datasets/fec/P00000001-ALL.csv')
print(fec.info())

print(fec.iloc[123456])

unique_cand = fec.cand_nm.unique()
print(unique_cand)
print(unique_cand[2])

parties = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Rimney, Mitt: ': ' Republican',
           'Santorum, Rick': 'Republican'}
print(fec.cand_nm[123456:123461])
print(fec.cand_nm[123456:123461].map(parties))
fec['party'] = fec.cand_nm.map(parties)
print(fec['party'].value_counts())

print((fec.contb_receipt_amt > 0).value_counts())

fec = fec[fec.contb_receipt_amt > 0]
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

print(fec.contbr_occupation.value_counts()[:10])

occ_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'UBFIRNATUIB REQYESTED': 'NOT PROVIDED',
               'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED',
               'C.E.O': 'CEO'}

f = lambda x: occ_mapping.get(x, x)
fec.contbr_occupation = fec.contbr_occupation.map(f)

emp_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'INFORMATION REQUESTED': 'NOT PROVIDED',
               'SELF': 'SELF-EMPLOYED',
               'SELF EMPLOYED': 'SELF-EMPLOYED'}

f = lambda x: emp_mapping.get(x, x)
fec.contbr_employer = fec.contbr_employer.map(f)

by_occupation = fec.pivot_table('contb_receipt_amt', index='contbr_occupation',
                                columns='party', aggfunc='sum')
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
print(over_2mm)

over_2mm.plot(kind='barh')
# plt.show()

def get_top_amounts(group, key, n=5):
    totals =group.groupby(key)['contb_receipt_amt'].sum()
    return totals.nlargest(n)

grouped = fec_mrbo.groupby('cand_nm')

print(grouped.apply(get_top_amounts, 'contbr_occupation', n=7))

print(grouped.apply(get_top_amounts, 'contbr_employer', n=10))

bins = np.array([0, 1, 10, 100, 1000, 10000,
                 100000, 1000000, 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt, bins)
print(labels)

grouped = fec_mrbo.groupby(['cand_nm', labels])
print(grouped.size().unstack(0))

bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
print(normed_sums)

normed_sums[:-2].plot(kind='barh')
plt.show()

grouped = fec_mrbo.groupby(['cand_nm', 'contbr_st'])
totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 100000]
print(totals[:10])

percent = totals.div(totals.sum(1), axis=0)
print(percent[:10])