import numpy as np
import pandas as pd
import string
import warnings
warnings.filterwarnings('ignore')

import requests



url = 'http://www.fundamentus.com.br/resultado.php'

header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"  
 }

r = requests.get(url, headers=header)

df = pd.read_html(r.text,  decimal=',', thousands='.')[0]

df

for coluna in ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Cresc. Rec.5a']:
  df[coluna] = df[coluna].str.replace('.', '')
  df[coluna] = df[coluna].str.replace(',', '.')
  df[coluna] = df[coluna].str.rstrip('%').astype('float') / 100



df = df[df['Liq.2meses'] > 1000000]

ranking = pd.DataFrame()
ranking['pos'] = range(1,151)
ranking['EV/EBIT'] = df[ df['EV/EBIT'] > 0 ].sort_values(by=['EV/EBIT'])['Papel'][:150].values
ranking['ROIC'] = df.sort_values(by=['ROIC'], ascending=False)['Papel'][:150].values
ranking['ROE'] = df.sort_values(by=['ROE'], ascending=False)['Papel'][:150].values
ranking['Mrg. Líq.'] = df[ df['Mrg. Líq.'] > 0 ].sort_values(by=['Mrg. Líq.'], ascending=False)['Papel'][:150].values
ranking['P/L'] = df.sort_values(by=['P/L'])['Papel'][:150].values
ranking['PSR'] = df.sort_values(by=['PSR'])['Papel'][:150].values
ranking['Div.Yield'] = df.sort_values(by=['Div.Yield'], ascending=False)['Papel'][:150].values
ranking['P/VP'] = df.sort_values(by=['P/VP'])['Papel'][:150].values
ranking['EV/EBITDA'] = df.sort_values(by=['EV/EBITDA'])['Papel'][:150].values
ranking['Dív.Brut/ Patrim.'] = df.sort_values(by=['Dív.Brut/ Patrim.'])['Papel'][:150].values

ranking

a = ranking.pivot_table(columns='EV/EBIT', values='pos')

b = ranking.pivot_table(columns='ROIC', values='pos')

c = ranking.pivot_table(columns='ROE', values='pos')

d = ranking.pivot_table(columns='Mrg. Líq.', values='pos')

e = ranking.pivot_table(columns='P/L', values='pos')

f = ranking.pivot_table(columns='PSR', values='pos')

g = ranking.pivot_table(columns='Div.Yield', values='pos')

h = ranking.pivot_table(columns='P/VP', values='pos')

i = ranking.pivot_table(columns='EV/EBITDA', values='pos')

j = ranking.pivot_table(columns='Dív.Brut/ Patrim.', values='pos')

t = pd.concat([a,b,c,d,e,f,g,h,i,j])
t

rank = t.dropna(axis=1).sum()
rank

rank.sort_values()[:80]

