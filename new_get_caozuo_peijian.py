#encoding=utf-8
from tqdm import tqdm
def get_peijian():
    with open('crf_result/new_tiaozhen_output.txt','r',encoding='utf-8') as fr:
        datas=fr.read()
        datas=datas.splitlines()
        datas=[data for data in datas if data!='']
    peijian_list=[]
    caozuo_list=[]
    a_str=''
    for sen in tqdm(datas):
        split_list=sen.split('\t')
        if split_list[2]=='B-PEI':
            if a_str!='':
                peijian_list.append(a_str)
                a_str=split_list[0]
            else:
                a_str=a_str+split_list[0]
        elif split_list[2]=='I-PEI':
            a_str = a_str + split_list[0]
        elif split_list[2]=='0':
            if a_str!='':
                peijian_list.append(a_str)
                a_str=''
    peijian_list=list(set(peijian_list))
    peijian_list=[peijian.strip(',') for peijian in peijian_list]
    new_peijian_list=[]
    for peijian in peijian_list:
        new_peijian_list.extend(peijian.split(','))
    new_peijian_list=list(set(new_peijian_list))
    with open('pro_data/tiaozhen_peijian.txt','w',encoding='utf-8') as fw:
        for peijian in new_peijian_list:
            fw.write(peijian+'\n')