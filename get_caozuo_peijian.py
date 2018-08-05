#encoding=utf-8
import pandas as pd
'''
这一部分是为了获得发现的配件词和操作词
'''
df=pd.read_csv('pro_data/allweibaoshuchu75-100.csv',encoding='gbk')
df=df.fillna(0)
caozuo_list=list(df['操作词'])
peijian_list=list(df['配件词'])

caozuo_list=[caozuo for caozuo in caozuo_list if caozuo!=0]
new_caozuo_list=[]
for caozuo in caozuo_list:
    new_caozuo_list.extend(caozuo.split())
new_caozuo_list=list(set(new_caozuo_list))
peijian_list=[peijian for peijian in peijian_list if peijian!=0]
new_peijian_list=[]
for peijian in peijian_list:
    new_peijian_list.extend(peijian.split())
new_peijian_list=list(set(new_peijian_list))
# print(len(new_peijian_list))
# print(len(new_caozuo_list))
with open('pro_data/peijian75-100.txt', 'w', encoding='utf-8') as fr:
    for data in new_peijian_list:
        fr.write(data + '\n')
with open('pro_data/caozuo75-100.txt', 'w', encoding='utf-8') as frs:
    for data in new_caozuo_list:
        frs.write(data + '\n')
# print(new_peijian_list[:10])