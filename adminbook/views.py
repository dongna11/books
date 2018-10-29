from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#登陆界面
from adminbook.models import *


def loginbook(request):
    return render(request,'login.html')

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
    return render(request,'pwd_Modify.html')


#读者档案管理
def managementbook(request):
    readers=TReader.objects.all()
    action = int(request.GET.get('action', '1'))
    if action == 1:
        return render(request,'reader.html',{'readers':readers})
    elif action == 0:
        readerid = int(request.GET.get('ID', ''))
        a=TReader.objects.get(id=readerid)
        a.rdelete=1
        a.save()
        return render(request, 'reader.html', {'readers': readers})
#读者类型管理
def typemanagementbook(request):
    readertypes = TReadertype.objects.all()
    action=int(request.GET.get('action','1'))
    if action==1:
        return render(request,'readerType.html',{'readertypes':readertypes})
    elif action==0:
        readertypeid=int(request.GET.get('ID',''))
        TReadertype.objects.get(id=readertypeid).delete()
        return render(request,'readerType.html',{'readertypes':readertypes})



def addreader(request):
    if request.method=='GET':
        readertypes = TReadertype.objects.all()
        return render(request,'addreader.html',{'readertypes':readertypes})
    else:
        rname=request.POST.get('rname','')
        rtype=request.POST.get('readertype','')
        rcardtype=request.POST.get('rcardtype','')
        rcardnum=request.POST.get('rcardnum','')
        rtel=request.POST.get('rtel','')
        remail=request.POST.get('remail','')
        rtypename=TReadertype.objects.get(rttype=rtype).id
        # print(rname,rtype,rcardtype,rcardnum,rtel,remail)
        sb=TReader.objects.create(rname=rname,rtype=TReadertype.objects.get(rttype=rtype),rcardtype=rcardtype,rcardnum=rcardnum,remail=remail,rtel=rtel)
        return HttpResponse('注册成功')


def addreadertype(request):
    if request.method=='GET':
        return render(request,'addreadertype.html')
    else:
        rttype=request.POST.get('rttype','')
        rtnum=request.POST.get('rtnum','')
        # print(rttype+rtnum)
        sb=TReadertype.objects.create(rttype=rttype,rtnum=rtnum)
        return HttpResponse('添加成功')


def changereader(request):
    if request.method=='GET':
        readerid=int(request.GET.get('ID',''))
        reader=TReader.objects.get(id=readerid)
        # print(reader)
        readertypes=TReadertype.objects.all()
        return render(request,'changereader.html',{'reader':reader,'readertypes':readertypes})
    else:
        readerid=request.POST.get('id','')
        rname=request.POST.get('rname','')
        rtype=request.POST.get('readertype','')
        rcardtype=request.POST.get('rcardtype','')
        rcardnum=request.POST.get('rcardnum','')
        rtel=request.POST.get('rtel','')
        remail=request.POST.get('remail','')
        rtypename=TReadertype.objects.get(rttype=rtype).id
        # print(rname,rtype,rcardtype,rcardnum,rtel,remail)
        sb=TReader.objects.filter(id=readerid).update(rname=rname,rtype=TReadertype.objects.get(rttype=rtype),rcardtype=rcardtype,rcardnum=rcardnum,remail=remail,rtel=rtel)
        return HttpResponse('修改成功')

def changereadertype(request):
    if request.method=='GET':
        readertypeid=request.GET.get('ID','')
        readertype=TReadertype.objects.get(id=readertypeid)
        return render(request,'changereadertype.html',{'readertype':readertype})
    else:
        rtid=request.POST.get('id','')
        rttype = request.POST.get('rttype', '')
        rtnum = request.POST.get('rtnum', '')
        # print(rttype+rtnum)
        sb = TReadertype.objects.filter(id=rtid).update(rttype=rttype, rtnum=rtnum)
        return HttpResponse('修改成功')