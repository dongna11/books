#coding=utf-8
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#登陆界面
from adminbook.models import *
from adminbook.models import TRoot



def loginbook(request):
    #接受数据
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        name=request.POST.get('name','')
        pwd=request.POST.get('pwd','')
        count=TRoot.objects.filter(rname=name,rpwd=pwd).count()
        #print(count)
        if count==1:
            return render(request,'main.html')
        else:
            return HttpResponse("密码或账号错误")

#首页
def indexbook(request):
    # 图书借阅表取得书名和借阅次数，并排序
    tbc = TBorrow.objects.values('bname').annotate(c=Count('*')).order_by('-c')[:3]
    # print(tbc)
    tbooks = []
    tbc_count = []
    for i in tbc:
        # 取得图书表的数据
        # print(i)
        tb = TBook.objects.filter(id=i['bname'])
        listtb = list(tb)
        tbooks.append(listtb)
        tbc_count.append(i['c'])
        # print(tbooks)

    newlist = []
    for ltb in tbooks:
        for lt in ltb:
            newlist.append(lt)
    # print(newlist)
    # print(tbc_count)
    return render(request, 'main.html', {'tbooks': newlist, 'tbc_count': tbc_count})

#图书归还
def returnbook(request):
    return render(request,'bookBack.html')

#图书借阅
def borrowingbook(request):
    return render(request,'bookBorrow.html')


#书架设置
def setupbook(request):
    return render(request,'bookcase.html')


#图书档案查询
def filesearchbook(request):
    return render(request,'bookQuery.html')


#图书续借
def renewalbook(request):
    return render(request,'bookRenew.html')

#图书类型设置
def typebook(request):
    booktypes=TBooktype.objects.all()
    return render(request,'bookType.html',{'booktypes':booktypes})


#图书借阅查询
def enquirybook(request):
    return render(request,'bookQuery.html')


#借阅到期提醒
def reminderbook(request):
    return render(request,'bremind.html')


#图书馆信息
def librarybook(request):
    return render(request,'library_modify.html')


#图书档案管理
def rankingbook(request):
    books=TBook.objects.all()
    return render(request,'book.html',{'books':books})


#管理员设置
def administratorbook(request):
    return render(request,'manager.html')


#参数设置
def parameterbook(request):
    return render(request,'parameter_modify.html')


#更改口令
def changepwdbook(request):
    rootname = request.POST.get('name', '')
    # print(rootname)

    newpwd = request.POST.get('pwd', '')
    checknewpwd = request.POST.get('pwd1', '')
    # print(rootname,newpwd,checknewpwd)
    tof = TRoot.objects.filter(rname=rootname)
    # print(tof)
    oldp = ''
    for i in tof:
        oldp = i.rpwd
        if oldp == request.POST.get('oldpwd', ''):
            if newpwd == checknewpwd:
                i.rpwd = newpwd
                i.save()
    # print(oldp)
    return render(request, 'pwd_Modify.html', {'oldp': oldp})


#读者档案管理
def managementbook(request):
    readers=TReader.objects.all()
    return render(request,'reader.html',{'readers':readers})

#读者类型管理
def typemanagementbook(request):
    readertypes=TReadertype.objects.all()
    return render(request,'readerType.html',{'readertypes':readertypes})


def addreader(request):
    if request.method=='GET':
        readertypes = TReadertype.objects.all()
        return render(request,'addreader.html',{'readertypes':readertypes})
    else:
        rname=request.POST.get('rname','')
        rtype=request.POST.get('rtype','')
        rcardtype=request.POST.get('rcardtype','')
        rcardnum=request.POST.get('rcardnum','')
        remail=request.POST.get('remail','')

        return HttpResponse('注册成功')
