from django.conf.urls import url,include
from django.contrib import admin
from .import views
urlpatterns = [
    url(r'^logins/',views.loginbook),
    url(r'^indexs/',views.indexbook),
    url(r'^returns/',views.returnbook),
    url(r'^borrowings/', views.borrowingbook),
    url(r'^setups/', views.setupbook),
    url(r'^filesearchs/', views.filesearchbook),
    url(r'^types/', views.typebook),
    url(r'^renewals/', views.renewalbook),
    url(r'^enquirys/', views.enquirybook),
    url(r'^reminders/',views.reminderbook),
    url(r'^librarys/',views.librarybook),
    url(r'^reminders/',views.reminderbook),
    url(r'^lendingrankings/',views.rankingbook),
    url(r'^administrators/',views.administratorbook),
    url(r'^changepwds/',views.changepwdbook),
    url(r'^managements/', views.managementbook),
    url(r'^typemanagements/', views.typemanagementbook),
]