#encoding=utf-8
import pandas as pd
'''
这一部分是对CRF++的输出结果进行处理从中得到被标记为配件词，操作词以及包含他们的文本
这里需要注意的是要根据打的标签不同进行调整
同时CRF++输出的文本格式不是utf-8的，导入之前要改编码格式
'''
def output_process(file_location):
    with open(file_location, 'r', encoding='utf-8') as fr:
        datas = fr.read()
        datas = datas.splitlines()
    content_list=[]
    biaozhu_list=[]
    content = ''
    biaozhu = []
    need_content_list=[]
    for data in datas:
        if data=='':
            content_list.append(content)
            biaozhu_list.append(biaozhu)
            content=''
            biaozhu = []
        else:
            content=content+data.split('\t')[0]
            biaozhu.append(data.split('\t')[2])
    caozuo_list = []
    peijian_list = []
    for i,datas in enumerate(biaozhu_list):
        caozuo_str=''
        peijian_str=''
        cao_tou=[]
        cao_wei=[]
        pei_tou=[]
        pei_wei=[]
        for k,data in enumerate(datas):
            if data=='B-CAO':
                cao_tou.append(k)
                for j in range(k+1,len(datas)):
                    if datas[j]!='I-CAO':
                        cao_wei.append(j)
                        break
                    if j==(len(datas)-1):
                        cao_wei.append(j+1)
            if data=='B-PEI':
                pei_tou.append(k)
                for j in range(k+1,len(datas)):
                    if datas[j]!='I-PEI':
                        pei_wei.append(j)
                        break
                    if j==(len(datas)-1):
                        pei_wei.append(j+1)
        if len(cao_tou)>0 or len(pei_tou)>0:
            need_content_list.append(content_list[i])
            for caotou,caowei in zip(cao_tou,cao_wei):
                caozuo_str=caozuo_str+content_list[i][caotou:caowei]+' '
            for peitou,peiwei in zip(pei_tou,pei_wei):
                peijian_str=peijian_str+content_list[i][peitou:peiwei]+' '
            caozuo_list.append(caozuo_str)
            peijian_list.append(peijian_str)
    return need_content_list,caozuo_list,peijian_list
if __name__ == '__main__':
    need_content_list, caozuo_list, peijian_list=output_process('crf_result/allweibaooutput75-100.txt')
    result=pd.DataFrame({
        '文本':need_content_list,
        '操作词':caozuo_list,
        '配件词':peijian_list
    })
    result.to_csv('pro_data/allweibaoshuchu75-100.csv',index=False,encoding='gbk')