# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from djqgrid.grid import  Grid
from djqgrid.columns import *
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from grids import *
from django.utils import timezone
# Create your models here.



class Vacation(models.Model):
    def __str__(self):
        return "from: " + str(self.start_date)+" to: "+ str(self.end_date)+ " description: "+ self.description  + " total period= " + str(self.total_period)

    #auto_increment_id = models.AutoField(primary_key=True, default=0)
    idd = models.IntegerField(default=0)
    employee = models.ForeignKey(User)
    description = models.CharField(max_length=500)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField( default=datetime.date.today)
    total_period = models.IntegerField(default=0)




