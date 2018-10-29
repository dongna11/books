# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class TBook(models.Model):
    bname = models.CharField(max_length=20)
    btype = models.ForeignKey('TBooktype', models.DO_NOTHING, db_column='btype')
    bwriter = models.ForeignKey('TWriter', models.DO_NOTHING, db_column='bwriter')
    bborrow = models.IntegerField()
    bpublish = models.ForeignKey('THouse', models.DO_NOTHING, db_column='bpublish')
    bbookrack = models.ForeignKey('TBookrack', models.DO_NOTHING, db_column='bbookrack')

    class Meta:
        managed = False
        db_table = 't_book'


class TBookrack(models.Model):
    brname = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_bookrack'


class TBooktype(models.Model):
    bttype = models.CharField(max_length=20)
    btday = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 't_booktype'


class TBorrow(models.Model):
    breader = models.ForeignKey('TReader', models.DO_NOTHING, db_column='breader')
    bname = models.ForeignKey(TBook, models.DO_NOTHING, db_column='bname')
    bborrowtime = models.DateTimeField()
    breturntime = models.DateTimeField()
    brealreturntime = models.DateTimeField(blank=True, null=True)
    badd = models.IntegerField()
    breturn = models.IntegerField()

    class Meta:
        managed = False
        db_table = 't_borrow'


class THouse(models.Model):
    hname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_house'


class TLibrary(models.Model):
    lname = models.CharField(max_length=20)
    lusername = models.CharField(max_length=20)
    ltel = models.CharField(max_length=20)
    lsite = models.CharField(max_length=50)
    lemail = models.CharField(max_length=20)
    lnet = models.CharField(max_length=50)
    lbirthday = models.CharField(max_length=20)
    lword = models.CharField(max_length=100)
    lmoney = models.CharField(max_length=20)
    ltime = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 't_library'


class TReader(models.Model):
    rname = models.CharField(max_length=20)
    rtype = models.ForeignKey('TReadertype', models.DO_NOTHING, db_column='rtype')
    rcardtype = models.CharField(max_length=20)
    rcardnum = models.CharField(max_length=20)
    rtel = models.CharField(max_length=20)
    remail = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 't_reader'


class TReadertype(models.Model):
    rttype = models.CharField(max_length=20)
    rtnum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 't_readertype'


class TRoot(models.Model):
    rname = models.CharField(max_length=20)
    rborrow = models.IntegerField()
    rsys = models.IntegerField()
    rreader = models.IntegerField()
    rbook = models.IntegerField()
    rinquiry = models.IntegerField()
    rpwd = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 't_root'


class TWriter(models.Model):
    wname = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 't_writer'
