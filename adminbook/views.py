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
    return render(request,'main.html')

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
    return render(request,'bookType.html')


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
    return render(request,'book.html')


#管理员设置
def administratorbook(request):
    return render(request,'manager.html')


#参数设置
def parameterbook(request):
    return render(request,'parameter_modify.html')


#更改口令
def changepwdbook(request):
    return render(request,'pwd_Modify.html')


#读者档案管理
def managementbook(request):
    readers=TReader.objects.all()
    return render(request,'reader.html',{'readers':readers})

#读者类型管理
def typemanagementbook(request):
    readertypes=TReadertype.objects.all()
    return render(request,'readerType.html',{'readertypes':readertypes})