#coding=utf-8
import random
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction
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
            return indexbook(request)
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
    if request.method == 'GET':
        tbok = TBook.objects.all()
        barcode = request.POST.get('barcode')
        return render(request,'bookBorrow.html',{'tbok':tbok})
    else:
        barcode = request.POST.get('barcode')
        noborder = request.POST.get('noborder')
        if barcode:
            tbok = TBook.objects.all()
            treader = TReader.objects.get(id=barcode)
            if noborder:
                cour = connection.cursor()
                # cour.execute("INSERT INTO `book`.`t_borrow` (breader,bname,bborrowtime,breturntime,brealreturntime,badd,breturn) VALUES (barcode,noborder,NOW(),'2018-11-7','2018-11-11','0','1')")
                cour.execute("INSERT INTO `book`.`t_borrow` VALUES (null,%s,%s,NOW(),'2018-11-7','2018-11-11','0','1')"%(barcode,noborder))
                rows = cour.fetchall()
                return HttpResponse('借阅完成')
            return render(request,'bookBorrow.html',{'treader':treader,'tbok':tbok})
        else:
            return render(request,'bookBorrow.html')
#书架设置
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
def libborrow(request,borrows):
    # 开始时间
    starttime = request.POST.get('sdate', '')
    starttime1 = int(starttime[:4] + starttime[5:7] + starttime[8:])
    print('starttime1:%s' % starttime1)
    # 终了时间
    endtime = request.POST.get('edate', '')
    endtime1 = int(endtime[:4] + endtime[5:7] + endtime[8:])
    print('endtime1:%s' % endtime1)
    jieyue = []
    for i in borrows:
        # 借阅时间
        borrtime = i.bborrowtime
        # print(type(borrtime))
        borrtime1 = datetime.datetime.strftime(borrtime, "%Y-%m-%d %H:%S:%M")
        # print(type(borrtime1))
        # print("borrtime1:%s"%borrtime1)
        borrtime2 = int(borrtime1[:4] + borrtime1[5:7] + borrtime1[8:10])
        # print('borrtime2:%s'%borrtime2)
        # 应还时间
        retutime = i.breturntime
        retutime1 = datetime.datetime.strftime(retutime, "%Y-%m-%d %H:%S:%M")
        retutime2 = int(retutime1[:4] + retutime1[5:7] + retutime1[8:10])
        if borrtime2 > starttime1 and retutime2 < endtime1:
            jieyue.append(i)
    return jieyue

def enquirybook(request):
    if request.method == 'GET':
        jieyue = TBorrow.objects.all()
        return render(request,'borrowQuery.html',{'jieyue':jieyue})
    else:
        #checkbox选项，是选择用什么查询，a:下拉框查询，b：根据时间查询
        checkbox_list = request.POST.getlist('flag',[])
        #下拉框选项目
        select1 = request.POST.get('f', '')
        #查询条件
        submit1 = request.POST.get('key', '')

        try:
            #两个查询条件
            if 'a' in checkbox_list and 'b' in checkbox_list:
                #图书条形码
                if select1 == 'barcode':
                    borrows = TBorrow.objects.filter(bname=submit1)
                    jieyue = libborrow(request,borrows)
                    return render(request, 'borrowQuery.html',{'jieyue':jieyue})

                #图书名称
                elif  select1 == 'bookname':
                    bookid = TBook.objects.filter(bname=submit1)
                    borrows = []
                    for bid in bookid:
                        borrow = TBorrow.objects.filter(bname=bid)
                        for i in borrow:
                            borrows.append(i)
                    jieyue = libborrow(request, borrows)

                    return render(request, 'borrowQuery.html', {'jieyue': jieyue})

                #读者条形码
                elif select1 == 'readerbarcode':
                    borrows = TBorrow.objects.filter(breader=submit1)
                    jieyue = libborrow(request, borrows)
                    return render(request, 'borrowQuery.html', {'jieyue': jieyue})

                #读者名称
                elif select1 == 'readername':
                    readers = TReader.objects.filter(rname=submit1)
                    borrows = []
                    for rid in readers:
                        borrow = TBorrow.objects.filter(breader=rid)
                        for i in borrow:
                            borrows.append(i)

                    jieyue = libborrow(request, borrows)
                    return render(request, 'borrowQuery.html', {'jieyue': jieyue})

            #只有复选框的条件
            elif 'a' in checkbox_list:
                # 图书条形码
                if select1 == 'barcode':
                    jieyue = TBorrow.objects.filter(bname=submit1)
                    return render(request, 'borrowQuery.html', {'jieyue': jieyue})
                #图书名称
                elif select1 == 'bookname':
                    bookid = TBook.objects.filter(bname=submit1)
                    jieyue = []
                    for bid in bookid:
                        borrow = TBorrow.objects.filter(bname=bid)
                        for i in borrow:
                            jieyue.append(i)
                    return render(request, 'borrowQuery.html', {'jieyue': jieyue})
                # 读者条形码
                elif select1 == 'readerbarcode':
                    jieyue = TBorrow.objects.filter(breader=submit1)
                    return render(request, 'borrowQuery.html', {'jieyue': jieyue})

                # 读者名称
                elif select1 == 'readername':
                    readers = TReader.objects.filter(rname=submit1)
                    jieyue = []
                    for rid in readers:
                        borrow = TBorrow.objects.filter(breader=rid)
                        for i in borrow:
                            jieyue.append(i)
                    return render(request, 'borrowQuery.html', {'jieyue': jieyue})

            #只有时间查询的条件
            elif 'b' in checkbox_list:
                borrows = TBorrow.objects.all()
                jieyue = libborrow(request, borrows)
                return render(request, 'borrowQuery.html', {'jieyue': jieyue})
        except:
            return render(request,'yichang.html')



#借阅到期提醒
def reminderbook(request):
    today = datetime.datetime.now()
    # print(type(today))
    today1 = datetime.datetime.strftime(today, "%Y-%m-%d %H:%S:%M")
    today2 = int(today1[:4]+today1[5:7]+today1[8:10])
    print(type(today2))
    print('today2:%s'%today2)
    borrows = TBorrow.objects.all()

    daoqi = []
    for bor in borrows:
        breturn = bor.breturn
        returntime = bor.breturntime
        # print(type(returntime))
        # print('returntime:%s'%returntime)
        returntime1 = datetime.datetime.strftime(returntime, "%Y-%m-%d %H:%S:%M")
        returntime2 = int(returntime1[:4]+returntime1[5:7]+returntime1[8:10])
        print(type(returntime2))
        # print('returntime2:%s'%returntime2)
        if returntime2<today2 and breturn==0:
            daoqi.append(bor)
    # print(daoqi)
    return render(request,'bremind.html',{'daoqi':daoqi,'today':today})
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
