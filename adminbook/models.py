# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

# 图书表（关联作者表、书架表、出版社表、图书类型表）
class TBook(models.Model):
    id = models.IntegerField(primary_key=True)#图书编号
    bname = models.CharField(max_length=20)#图书名称
    btype = models.ForeignKey('TBooktype', models.DO_NOTHING, db_column='btype')#图书类型编号（与图书类型表关联）
    bwriter = models.ForeignKey('TWriter', models.DO_NOTHING, db_column='bwriter')#作者编号（与作者表关联）
    bborrow = models.IntegerField()#借阅标记（布尔值）
    bpublish = models.ForeignKey('THouse', models.DO_NOTHING, db_column='bpublish')#出版社标号（与出版社表关联）
    bbookrack = models.ForeignKey('TBookrack', models.DO_NOTHING, db_column='bbookrack')#书架编号（与书架表关联）

    class Meta:
        managed = False
        db_table = 't_book'

# 书架表
class TBookrack(models.Model):
    id = models.IntegerField(primary_key=True)#书架编号
    brname = models.CharField(max_length=20, blank=True, null=True)#书架名称

    class Meta:
        managed = False
        db_table = 't_bookrack'

#图书类型表
class TBooktype(models.Model):
    id = models.IntegerField(primary_key=True)#图书类型编号
    bttype = models.CharField(max_length=20)#图书类型
    btday = models.CharField(max_length=20)#可借天数

    class Meta:
        managed = False
        db_table = 't_booktype'

#图书借阅表（关联图书表和读者表）
class TBorrow(models.Model):
    id = models.IntegerField(primary_key=True)
    breader = models.ForeignKey('TReader', models.DO_NOTHING, db_column='breader')#读者编号（与读者表关联）
    bname = models.ForeignKey(TBook, models.DO_NOTHING, db_column='bname')#书名编号（与图书表关联）
    bborrowtime = models.DateTimeField()#借书时间
    breturntime = models.DateTimeField()#应还时间
    brealreturntime = models.DateTimeField()#实际归还时间
    badd = models.IntegerField()#是否借阅标志（布尔值）
    breturn = models.IntegerField()#是否归还标志（布尔值）

    class Meta:
        managed = False
        db_table = 't_borrow'

#出版社表
class THouse(models.Model):
    id = models.IntegerField(primary_key=True)#出版社编号
    hname = models.CharField(max_length=50)#出版社名称

    class Meta:
        managed = False
        db_table = 't_house'

#图书馆信息表
class TLibrary(models.Model):
    id = models.IntegerField(primary_key=True)
    lname = models.CharField(max_length=20)#图书馆名称
    lusername = models.CharField(max_length=20)#馆长姓名
    ltel = models.CharField(max_length=20)#联系电话
    lsite = models.CharField(max_length=50)#联系地址
    lemail = models.CharField(max_length=20)#电子邮件
    lnet = models.CharField(max_length=50)#网站
    lbirthday = models.CharField(max_length=20)#建馆时间
    lword = models.CharField(max_length=100)#简介
    lmoney = models.CharField(max_length=20)#办证费
    ltime = models.CharField(max_length=20)#证件有效期限

    class Meta:
        managed = False
        db_table = 't_library'

#读者表（与读者类型关联）
class TReader(models.Model):
    id = models.IntegerField(primary_key=True)#读者编号
    rname = models.CharField(max_length=20)#读者姓名
    rtype = models.ForeignKey('TReadertype', models.DO_NOTHING, db_column='rtype')#读者类型编号（与读者类型表关联）
    rcardtype = models.CharField(max_length=20)#证件类型
    rcardnum = models.CharField(max_length=20)#证件号码
    rtel = models.CharField(max_length=20)#联系电话
    remail = models.CharField(max_length=30)#电子邮件

    class Meta:
        managed = False
        db_table = 't_reader'

#读者类型表
class TReadertype(models.Model):
    id = models.IntegerField(primary_key=True)#读者类型编号
    rttype = models.CharField(max_length=20)#读者类型
    rtnum = models.IntegerField()#可借天数

    class Meta:
        managed = False
        db_table = 't_readertype'

#管理员表
class TRoot(models.Model):
    id = models.IntegerField(primary_key=True)#管理员编号
    rname = models.CharField(max_length=20)#管理员账号
    rborrow = models.IntegerField()#图书借还权限（布尔值）
    rsys = models.IntegerField()#系统设置权限（布尔值）
    rreader = models.IntegerField()#读者管理权限（布尔值）
    rbook = models.IntegerField()#图书管理权限（布尔值）
    rinquiry = models.IntegerField()#系统查询权限（布尔值）
    rpwd = models.CharField(max_length=50)#密码

    class Meta:
        managed = False
        db_table = 't_root'

#作者表
class TWriter(models.Model):
    id = models.IntegerField(primary_key=True)#作者编号
    wname = models.CharField(max_length=30)#作者姓名

    class Meta:
        managed = False
        db_table = 't_writer'
