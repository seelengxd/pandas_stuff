import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


dataset = pd.read_csv("data.csv", index_col=0)
dataset.columns = ['gender','age','area','value']
dataset.area = dataset.area.str.replace("- Total","")

total = dataset.copy()
total = total[(total.gender == 'Total') & (total.age == 'Total')]
                                                                     
byAge = dataset.copy()
byAge = byAge[(byAge.gender == 'Total') & (byAge.age != 'Total' )]

total = total.set_index('area')
total.drop(columns=['gender','age'], inplace=True)
total.columns = ['total']

byAge = byAge.pivot(index='area',columns='age', values='value')

test = byAge.join(total, how='inner')
test.fillna(0, inplace=True)

test['Elderly'] = byAge['65 - 69'] + byAge['70 - 74'] + byAge['80 - 84'] + byAge['85 & Over']
test['Elderly %'] = test.Elderly / test.total * 100

test.sort_values('Elderly %',inplace=True)
test.dropna(inplace=True)

test.reset_index(inplace=True)
test.plot.barh(y='Elderly %')
plt.figure(figsize=(20.0, 10.0))
sns.barplot(data=test, x="Elderly %", y="area", edgecolor="black")

plt.xlabel('% of elderly in that planning area')
plt.title(': ]')
plt.savefig('graph.png')

