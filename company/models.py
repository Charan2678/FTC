# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()

    class Meta:
        db_table = "company"
        managed = False

    def __str__(self):
        return self.company_name
