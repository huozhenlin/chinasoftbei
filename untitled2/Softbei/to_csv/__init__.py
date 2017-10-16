#coding:utf8
import pandas as pd

df = pd.read_csv(r'C:\untitled2\Softbei\to_csv\before_csv\before_news.csv')
title = list(df['标题'])

print title