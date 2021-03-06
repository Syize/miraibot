#!/usr/bin/python3
#这个模块用于权限的检查、更改，包括个人op权限和群组功能开关
from src.ReplyTryRun import TryRun
from src import GlobalSet

@TryRun
def Access(target,App='',mode='check',status=''):
    path='src/Cache/'
    from os import listdir,mkdir
    from json import loads,dumps
    from copy import deepcopy
    
    target=str(target)
    template={
            'Open':True,
            'Setu':False,
            'Weather':True,
            'PicMark':True,
            'PSetu':True,
            'Reply':True,
            'ZhaoXin':False,
            'TimeSend':False,
            'NoTalk':True
            }
    if 'src' not in lisdir():
        mkdir('src')
        print('\n初始化缓存文件夹')
    if 'Cache' not in listdir('src'):
        mkdir(path)
        print('\n创建缓存文件夹\n*************\n')

    if 'SenderAccess' not in dir(GlobalSet):
        if 'SenderAccess' not in listdir(path):
            GlobalSet.SenderAccess=[GlobalSet.AdminQQ]
            with open(path+'SenderAccess','w') as f:
                f.write(GlobalSet.AdminQQ)
        else:
            with open(path+'SenderAccess','r') as f:
                GlobalSet.SenderAccess=f.read().split()
    
    if 'GroupAccess' not in dir(GlobalSet):
        if 'GroupAccess' not in listdir(path):
            GlobalSet.GroupAccess={}
        else:
            with open(path+'GroupAccess','r') as f:
                GlobalSet.GroupAccess=loads(f.read())

    if App:
        if target not in GlobalSet.GroupAccess:
            print('\nQQ群'+target+'无配置，使用默认设置生成\n****************\n')
            GlobalSet.GroupAccess[target]=deepcopy(template)
            with open(path+'GroupAccess','w') as f:
                f.write(dumps(GlobalSet.GroupAccess))
        templatekey=set(template.keys())
        groupkey=set(GlobalSet.GroupAccess[target].keys())
        a=templatekey^groupkey
        if a:
            for i in list(a):
                if i in GlobalSet.GroupAccess[target]:
                    GlobalSet.GroupAccess[target].pop(i)
                else:
                    GlobalSet.GroupAccess[target][i]=template[i]
        if mode=='check':
            return GlobalSet.GroupAccess[target][App]
        elif mode=='set':
            if type(status)!=bool:
                raise Exception('错误的参数 status:',status)
            GlobalSet.GroupAccess[target][App]=status
            with open(path+'GroupAccess','w') as f:
                f.write(dumps(GlobalSet.GroupAccess))
            return '设置成功'
        elif mode=='status':
            text=''
            for i in GlobalSet.GroupAccess[target]:
                text=text+i+': '+str(GlobalSet.GroupAccess[target][i])+'\n'
            return text.strip('\n')
        else:
            raise Exception('错误的参数 mode:'+mode)
        with open(path+'GroupAccess','w') as f:
            f.write(dumps(GlobalSet.GroupAccess))
    else:
        if mode=='check':
            if target in GlobalSet.SenderAccess:
                return True
            else:
                return False
        elif mode=='set':
            if type(status)!=bool:
                raise Exception('错误的参数 status:',status)
            if status:
                if target in GlobalSet.SenderAccess:
                    return '目标已有管理员权限'
                else:
                    GlobalSet.SenderAccess.append(target)
                    with open(path+'SenderAccess','w') as f:
                        for i in GlobalSet.SenderAccess:
                            f.write(i+' ')
                    return '更改成功'
            else:
                if target in GlobalSet.SenderAccess:
                    GlobalSet.SenderAccess.remove(target)
                    with open(path+'SenderAccess','w') as f:
                        for i in GlobalSet.SenderAccess:
                            f.write(i+' ')
                    return '更改成功'
                else:
                    return '目标无权限'
        else:
            raise Exception('错误的参数 mode:'+mode)
