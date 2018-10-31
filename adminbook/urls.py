from django.conf.urls import url,include
from django.contrib import admin
from .import views
urlpatterns = [
    url(r'^logins/',views.loginbook),
    url(r'^indexs/',views.indexbook),
    url(r'^returns/',views.returnbook),
    url(r'^borrowings/', views.borrowingbook),
    #书架设置（删除书架）
    url(r'^setups/', views.setupbook),
    #添加书架
    url(r'^addbookcase/',views.addbookcase),
    #修改书架
    url(r'^changebookcase/',views.changebookcase),
    url(r'^filesearchs/', views.filesearchbook),
    url(r'^filesearchs/',views.filesearchbook),
    url(r'^types/', views.typebook),
    url(r'^renewals/', views.renewalbook),
    url(r'^enquirys/', views.enquirybook),
    url(r'^reminders/',views.reminderbook),
    url(r'^librarys/',views.librarybook),
    url(r'^lendingrankings/',views.rankingbook),
    url(r'^administrators/',views.administratorbook),
    url(r'^changepwds/',views.changepwdbook),
    #读者档案管理
    url(r'^managements/', views.managementbook),
    #读者类型管理
    url(r'^typemanagements/', views.typemanagementbook),
    url(r'^addreader/',views.addreader),
    url(r'^addreadertype/',views.addreadertype),
    url(r'changereader/',views.changereader),
    url(r'changereadertype/',views.changereadertype),
    url(r'addbook/',views.addbook),
    url(r'changebook/',views.changebook),
    url(r'addbooktype/',views.addbooktype),
    url(r'changebooktype',views.changebooktype),
    url(r'^parameters/',views.parameterbook),
]