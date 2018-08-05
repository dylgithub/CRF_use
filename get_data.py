#encoding=utf-8
import pandas as pd
import jieba
from tqdm import tqdm
'''
这一部分是对文件的预处理，把原始数据转换成满足CRF++需求的文本格式
先对文本进行切词再读取存有切词数据的文本
再调用get_train_data，最后调用get_txt获得可用于crf++训练的文本
'''
def get_content():
    df=pd.read_csv('data/delete_zifu_set_content.csv',encoding='utf-8')
    return list(df['content'])
def get_all_weibao_content():
    with open('data/4159important_peijian.txt','r',encoding='utf-8') as fr:
        datas=fr.read()
        datas=datas.splitlines()
        return datas
def get_need_content():
    df=pd.read_csv('data/need_content.csv',encoding='utf-8')
    return list(df['content'])
def get_cut_content():
    df=pd.read_csv('data/cut_siliang_content.csv',encoding='utf-8')
    return list(df['content'])
def get_caozuo():
    with open('data/new_caozuo_list.txt','r',encoding='utf-8') as fr:
        datas=fr.read()
        datas=datas.splitlines()
        return datas
def get_peijian():
    df=pd.read_csv('data/final_pejian.csv',encoding='gbk')
    return list(df['peijian'])
def get_contain_peijian_caozuo_content():
    content_list=get_content()
    caozuo_list=get_caozuo()
    peijian_list=get_peijian()
    need_content_list=[]
    num=0
    for content in tqdm(content_list):
        if num>25000:
            break
        flag=False
        for caozuo in caozuo_list:
            if flag:
                break
            if str(caozuo) in str(content):
                for peijian in peijian_list:
                    if str(peijian) in str(content):
                        need_content_list.append(content)
                        num=num+1
                        flag=True
                        break
    result=pd.DataFrame({
        'content':need_content_list
    })
    result.to_csv('data/need_content.csv',encoding='utf-8',index=False)
def get_jie_cut_content():
    need_content_list=get_all_weibao_content()
    jieba.load_userdict('dict/my_dict.txt')
    cut_content=[]
    for content in tqdm(need_content_list):
        cut_content.append(' '.join(jieba.lcut(content)))
    result = pd.DataFrame({
        'content': cut_content
    })
    result.to_csv('data/cut_siliang_content.csv', encoding='utf-8', index=False)
def get_train_data():
    cut_content=get_cut_content()
    caozuo_list = get_caozuo()
    peijian_list = get_peijian()
    new_need=[]
    for content in tqdm(cut_content):
        cut_list=content.split()
        for word in cut_list:
            if word in caozuo_list:
                for i in range(len(word)):
                    if i==0:
                        new_need.append(word[i]+' '+'B-CAO')
                    else:
                        new_need.append(word[i] + ' ' + 'I-CAO')
            elif word in peijian_list:
                for i in range(len(word)):
                    if i==0:
                        new_need.append(word[i]+' '+'B-PEI')
                    else:
                        new_need.append(word[i] + ' ' + 'I-PEI')
            else:
                for i in range(len(word)):
                    new_need.append(word[i]+' '+'O')
        new_need.append(' ')
    result = pd.DataFrame({
        'content': new_need
    })
    result.to_csv('data/siliang_train_data.csv', encoding='utf-8', index=False)
def get_tes_data():
    cut_content = get_cut_content()[750000:1000000]
    new_need = []
    for content in tqdm(cut_content):
        cut_list = content.split()
        for word in cut_list:
            for i in range(len(word)):
                new_need.append(word[i] + ' ' + 'O')
        new_need.append(' ')
    result = pd.DataFrame({
        'content': new_need
    })
    result.to_csv('test_data/dan_test_data75-100.csv', encoding='utf-8', index=False)
#因为切词之后是存在了csv中,用“”扩住了，传入前去除“”
def get_txt(open_file_location,save_file_location):
    with open(open_file_location,'r',encoding='utf-8') as fr:
        datas=fr.read()
        datas=datas.splitlines()[1:]
    with open(save_file_location,'w',encoding='utf-8') as fr2:
        for word in datas:
            if word==' ':
                fr2.write('\n')
            else:
                fr2.write(word+'\n')
if __name__ == '__main__':
    # get_tes_data()
    # get_jie_cut_content()
    # get_train_data()
    get_txt('data/siliang_train_data.csv','data/siliangtrain.data')
