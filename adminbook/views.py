from django.shortcuts import render

# Create your views here.
#登陆界面
def loginbook(request):
    return render(request,'login.html')

#首页
def indexbook(request):
    return render(request,'main.html.html')


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
    return render(request,'reader.html')

#读者类型管理
def typemanagementbook(request):
    return render(request,'readerType.html')