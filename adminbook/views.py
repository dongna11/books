#coding=utf-8
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import time,datetime
# Create your views here.

from adminbook.models import *
from adminbook.models import TRoot
import jsonpickle

#登陆界面
def loginbook(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        name=request.POST.get('name','')
        pwd=request.POST.get('pwd','')
        userList=TRoot.objects.filter(rname=name,rpwd=pwd)
        #print(count)
        if userList:
            request.session['user'] = jsonpickle.dumps(userList[0])
            return render(request,'main.html')
        else:
            return render(request,'login.html')

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
    if request.method=="GET":
        return render(request,'bookBack.html')
    else:
        borrow=request.POST.getlist('borrow','')
        # print(borrow)
        if borrow:
            for x in borrow:
                book=TBorrow.objects.get(id=x).bname
                TBorrow.objects.filter(id=x).update(breturn=1,brealreturntime=datetime.datetime.now())
                book.bborrow=0
                book.save()
        readerid=request.POST.get('readerid','')
        readers=TReader.objects.filter(id=readerid)
        for a in readers:
            reader=a
        bookes=TBorrow.objects.filter(breader=reader.id)
        return render(request,'bookBack.html',{'reader':reader,"bookes":bookes})
#图书借阅
def borrowingbook(request):
    return render(request,'bookBorrow.html')

#图书档案查询
def filesearchbook(request):
    if request.method == 'GET':
        #所有图书对象
        allbooks = TBook.objects.all()
        return render(request,'bookQuery.html',{'allbooks':allbooks})
    else:
        select1 = request.POST.get('f','')
        submit1 = request.POST.get('key','')
        try:
            if select1 == 'barcode':
                allbooks = TBook.objects.filter(id=submit1)
                return render(request, 'bookQuery.html', {'allbooks': allbooks})
            elif select1 == 'typename':
                leibieid = TBooktype.objects.get(bttype=submit1).id
                allbooks = TBook.objects.filter(btype=leibieid)
                return render(request, 'bookQuery.html', {'allbooks': allbooks})
            elif select1 == 'bookname':
                allbooks = TBook.objects.filter(bname=submit1)
                return render(request, 'bookQuery.html', {'allbooks': allbooks})
            elif select1 == 'publishing':
                chubansheid = THouse.objects.get(hname=submit1).id
                allbooks = TBook.objects.filter(bpublish=chubansheid)
                return render(request, 'bookQuery.html', {'allbooks': allbooks})
            elif select1 == 'bookcasename':
                shujiaid = TBookrack.objects.get(brname=submit1).id
                allbooks = TBook.objects.filter(bbookrack=shujiaid)
                return render(request,'bookQuery.html',{'allbooks':allbooks})
        except:
            return render(request,'yichang.html')


#图书续借
def renewalbook(request):
    if request.method=='GET':
        return render(request,'bookRenew.html')
    else:
        renew=request.POST.getlist('renew','')
        if renew:
            for x in renew:
                # book=TBook.objects.get(id=x)
                time=TBorrow.objects.get(id=x).breturntime
                TBorrow.objects.filter(id=x).update(badd=1,breturntime=time+datetime.timedelta(days=30))
        readerid=request.POST.get('reader','')
        readers=TReader.objects.filter(id=readerid)
        for x in readers:
            reader=x
        bookes=TBorrow.objects.filter(breader=reader)
        return render(request,'bookRenew.html',{'bookes':bookes,'reader':reader})

#图书类型设置
def typebook(request):
    booktypes=TBooktype.objects.all()
    action=int(request.GET.get('action','1'))
    if action == 1:
        return render(request,'bookType.html',{'booktypes':booktypes})
    elif action == 0:
        booktypeid=request.GET.get('ID','')
        TBooktype.objects.get(id=booktypeid).delete()
        return render(request, 'bookType.html', {'booktypes': booktypes})
#图书借阅查询
def enquirybook(request):
    return render(request,'bookQuery.html')


#借阅到期提醒
def reminderbook(request):
    return render(request,'bremind.html')
#图书馆信息
def librarybook(request):
    if request.method == 'GET':
        tlibrary = TLibrary.objects.first()
        return render(request, 'library_modify.html', {'tlibrary': tlibrary})
    else:
        libraryname = request.POST.get('libraryname', '')
        curator = request.POST.get('curator', '')
        tel = request.POST.get('tel', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        url = request.POST.get('url', '')
        createDate = request.POST.get('createDate', '')
        introduce = request.POST.get('introduce', '')
        tlibrary = TLibrary.objects.first()
        tlibrary.lname = libraryname
        tlibrary.lusername = curator
        tlibrary.ltel = tel
        tlibrary.lsite = address
        tlibrary.lemail = email
        tlibrary.lnet = url
        tlibrary.lbirthday = createDate
        tlibrary.lword = introduce
        tlibrary.save()
        return HttpResponse('保存成功')


#图书档案管理
def rankingbook(request):
    books=TBook.objects.all()
    action = int(request.GET.get('action', '1'))
    if action==1:
        return render(request,'book.html',{'books':books})
    elif action==0:
        bookid=request.GET.get('ID','')
        a=TBook.objects.get(id=bookid)
        a.bdelete=1
        a.save()
        return render(request,'book.html',{'books':books})


#管理员设置
def administratorbook(request):

    return render(request,'manager.html')


#参数设置
def parameterbook(request):
    if request.method == 'GET':
        books = TLibrary.objects.first()
        return render(request,'parameter_modify.html',{'books':books})
    else:
        cost = request.POST.get('cost','')
        validity = request.POST.get('validity','')
        tlis = TLibrary.objects.first()
        tlis.lmoney = cost
        tlis.ltime = validity
        tlis.save()
        return HttpResponse('完成')
#更改口令
def changepwdbook(request):
    rootname = request.POST.get('name', '')
    # print(rootname)
    newpwd = request.POST.get('pwd', '')
    checknewpwd = request.POST.get('pwd1', '')
    # print(rootname,newpwd,checknewpwd)
    tof = TRoot.objects.filter(rname=rootname)
    #print(tof)
    oldp = ''
    for i in tof:
        print(i)
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
    action = int(request.GET.get('action', '1'))
    if action == 1:
        return render(request,'reader.html',{'readers':readers})
    elif action == 0:
        readerid = request.GET.get('ID', '')
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
        sb=TReader.objects.create(rname=rname,rtype=TReadertype.objects.get(rttype=rtype),rcardtype=rcardtype,rcardnum=rcardnum,remail=remail,rtel=rtel,rdelete=0)
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
        readerid=request.GET.get('ID','')
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
        sb=TReader.objects.filter(id=readerid).update(rname=rname,rtype=TReadertype.objects.get(rttype=rtype),rcardtype=rcardtype,rcardnum=rcardnum,remail=remail,rtel=rtel,rdelete=0)
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


#书架设置(包括删除)
def setupbook(request):
    action=request.GET.get('action','1')
    if action == '1':
        bookcase = TBookrack.objects.all()
        return render(request, 'bookcase.html', {'bookcase': bookcase})
    if action == '0':
        id = request.GET.get('ID', '')
        # print(id)
        TBookrack.objects.get(id=id).delete()
        bookcase = TBookrack.objects.all()
        return render(request, 'bookcase.html', {'bookcase': bookcase})

#添加书架
def addbookcase(request):
    if request.method=="GET":
        return render(request,'addbookcase.html')
    else:
        brname=request.POST.get('brname','')
        TBookrack.objects.create(brname=brname)
        return HttpResponse('添加成功')
#修改书架
def changebookcase(request):
    if request.method=='GET':
        bookcaseid=request.GET.get('ID','')
        changebookcase= TBookrack.objects.get(id=bookcaseid)
        return render(request,'changebookcase.html',{'changebookcase':changebookcase})
    else:
        bid = request.POST.get('id','')
        brname=request.POST.get('brname','')

        bchange = TBookrack.objects.get(id=bid)
        bchange.brname = brname
        bchange.save()

        return HttpResponse('修改成功')


def addbook(request):
    if request.method=='GET':
        # bookes=TBook.objects.all()
        booktypes=TBooktype.objects.all()
        bookrackes=TBookrack.objects.all()
        # writers=TWriter.objects.all()
        return render(request,'addbook.html',{'booktypes':booktypes,'bookrackes':bookrackes})
    else:
        bname=request.POST.get('bname','')
        btype=request.POST.get('booktype','')
        bwriter=request.POST.get('bwriter','')
        bpublish=request.POST.get('bpublish','')
        bbookrack=request.POST.get('bookrack','')
        # print(bname+btype+bwriter+bpublish+bbookrack)
        try:
            publish =THouse.objects.get(hname=bpublish)
        except THouse.DoesNotExist:
            publish = THouse.objects.create(hname=bpublish)
        try:
            writer =TWriter.objects.get(wname=bwriter)
        except TWriter.DoesNotExist:
            writer = TWriter.objects.create(wname=bwriter)
        TBook.objects.create(bname=bname,btype=TBooktype.objects.get(id=btype),bbookrack=TBookrack.objects.get(id=bbookrack),bborrow=0,bdelete=0,bwriter=writer,bpublish=publish)
        return HttpResponse('添加成功')


def changebook(request):
    if request.method=="GET":
        bookid=request.GET.get('ID','')
        # print(bookid)
        # # print(type(bookid))
        # bookid=int(bookid)
        book=TBook.objects.get(id=bookid)
        booktypes=TBooktype.objects.all()
        bookracks=TBookrack.objects.all()
        writer=TBook.objects.get(id=bookid).bwriter
        publish=TBook.objects.get(id=bookid).bpublish
        return render(request,'changebook.html',{'book':book,'booktypes':booktypes,'bookracks':bookracks,'writer':writer,'publish':publish})
    else:
        bname=request.POST.get('bname','')
        booktype=request.POST.get('booktype','')
        bookrack=request.POST.get('bookrack','')
        bpublish=request.POST.get('bpublish','')
        bwriter=request.POST.get('bwriter','')
        id=request.POST.get('id','')
        # print(bname+bookrack+booktype+bpublish+bwriter)
        try:
            publish =THouse.objects.get(hname=bpublish)
        except THouse.DoesNotExist:
            publish = THouse.objects.create(hname=bpublish)
        try:
            writer =TWriter.objects.get(wname=bwriter)
        except TWriter.DoesNotExist:
            writer = TWriter.objects.create(wname=bwriter)
        sb=TBook.objects.filter(id=id).update(bname=bname,btype=booktype,bwriter=writer,bpublish=publish,bbookrack=bookrack)
        return HttpResponse('修改成功')


def addbooktype(request):
    if request.method=="GET":
        return render(request,'addbooktype.html')
    else:
        bttype=request.POST.get('bttype','')
        btnum=int(request.POST.get('btnum',''))
        try:
            type =TBooktype.objects.get(bttype=bttype)
        except TBooktype.DoesNotExist:
            type = TBooktype.objects.create(bttype=bttype,btday=btnum)
        type.btday=btnum
        type.save()
        return HttpResponse('添加成功')


def changebooktype(request):
    if request.method=="GET":
        booktypeid=request.GET.get('ID','')
        booktype=TBooktype.objects.get(id=booktypeid)
        return render(request,'changebooktype.html',{'booktype':booktype})
    else:
        id=request.POST.get('id','')
        bttype=request.POST.get('bttype','')
        btday=request.POST.get('btday','')
        sb=TBooktype.objects.filter(id=id).update(bttype=bttype,btday=btday)
        return HttpResponse('修改成功')
