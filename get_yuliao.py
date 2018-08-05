#encoding=utf-8
'''
这一部分是把CRF++训练格式的数据转换为便于检查的部分
'''
with open('data/siliangtrain.data','r',encoding='utf-8') as fr:
    datas=fr.read()
    datas=datas.splitlines()
with open('data/siliangbiaozhu.txt','w',encoding='utf-8') as fr2:
    wri_str = ''
    for data in datas:
        if data=='':
            fr2.write('\n')
            fr2.write(wri_str)
            wri_str=''
        else:
            wri_str=wri_str+data.split()[0]+'/'+data.split()[1]+'  '
with open('data/siliangbiaozhu.txt','r',encoding='utf-8') as fr:
    datas=fr.read()
    datas=datas.splitlines()
shuchu_list=[]
for data in datas:  #遍历文本列表
    ju_str = ''
    split_list=data.split('  ')
    split_list=[word for word in split_list if word!='']
    for i,word in enumerate(split_list):
        if word.split('/')[1]=='B-PEI':
            if (i - 1) < 0:
                ci_str = ''
            else:
                if split_list[i - 1].split('/')[1] == 'O':
                    ci_str = ' '
                else:
                    ci_str = ''
            ci_str=ci_str+word.split('/')[0]
            for j in range(i+1,len(split_list)):
                if split_list[j].split('/')[1]!='I-PEI':
                    break
                else:
                    ci_str=ci_str+split_list[j].split('/')[0]
            ju_str = ju_str + ci_str+' '
        elif word.split('/')[1]=='B-CAO':
            if (i-1)<0:
                ci_str=''
            else:
                if split_list[i-1].split('/')[1]=='O':
                    ci_str=' '
                else:
                    ci_str=''
            ci_str=ci_str+word.split('/')[0]
            for j in range(i+1,len(split_list)):
                if split_list[j].split('/')[1]!='I-CAO':
                    break
                else:
                    ci_str=ci_str+split_list[j].split('/')[0]
            ju_str = ju_str + ci_str+' '
        elif word.split('/')[1]=='O':
            ju_str=ju_str+word.split('/')[0]
    shuchu_list.append(ju_str)
with open('pro_data/siliangyuliao.txt','w',encoding='utf-8') as fr2:
    for shuchu in shuchu_list:
        fr2.write(shuchu+'\n')



