from django.db import models

# -*- coding:utf-8 -*-
class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    name = models.CharField(max_length=20)
