#coding=utf-8
from django.core.paginator import Paginator
from django.db.models import Count
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from adminbook.models import *
# from adminbook.models import TRoot


#登陆界面
def loginbook(request):
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
    return render(request, 'bookBorrow.html')


#书架设置
def setupbook(request):
    return render(request,'bookcase.html')


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
                return render(request, 'bookQuery.html', {'allbooks': allbooks})
        except:
            return render(request,'yichang.html')


#图书续借
def renewalbook(request):
    return render(request,'bookRenew.html')

#图书类型设置
def typebook(request):
    booktypes=TBooktype.objects.all()
    return render(request,'bookType.html',{'booktypes':booktypes})


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
        borrtime1 = datetime.strftime(borrtime, "%Y-%m-%d %H:%S:%M")
        # print(type(borrtime1))
        # print("borrtime1:%s"%borrtime1)
        borrtime2 = int(borrtime1[:4] + borrtime1[5:7] + borrtime1[8:10])
        # print('borrtime2:%s'%borrtime2)
        # 应还时间
        retutime = i.breturntime
        retutime1 = datetime.strftime(retutime, "%Y-%m-%d %H:%S:%M")
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
    today = datetime.now()
    # print(type(today))
    today1 = datetime.strftime(today, "%Y-%m-%d %H:%S:%M")
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
        returntime1 = datetime.strftime(returntime, "%Y-%m-%d %H:%S:%M")
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
    oldpwd = request.POST.get('oldpwd', '')
    newpwd = request.POST.get('pwd', '')
    checknewpwd = request.POST.get('pwd1', '')
    print(rootname,newpwd,checknewpwd)
    tof = TRoot.objects.filter(rname=rootname)
    # print(tof)
    # print(tof.rpwd)
    oldp = ''
    for i in tof:
        oldp = i.rpwd
        if oldp == oldpwd:
            if newpwd == checknewpwd:
                i.rpwd = newpwd
                i.save()
    print(oldp)
    return render(request, 'pwd_Modify.html',{'oldp':oldp})


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