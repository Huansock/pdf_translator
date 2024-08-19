from django.db import models
# Create your models here.
class Translator (models.Model):
    id = models.AutoField(blank=True,primary_key=True )
    src_lang = models.CharField(max_length=255 , verbose_name="source language")
    dst_lang = models.CharField(max_length=255, verbose_name='destination language')
    pdf = models.FileField(upload_to='pdfs/',verbose_name="pdf")
    api_key = models.CharField(max_length=255, verbose_name="api_key")
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True , verbose_name="created_at")