from django.db import models
# Create your models here.
class Translator (models.Model):
    id = models.AutoField(blank=True,primary_key=True)
    src_lang = models.CharField(max_length=255 , verbose_name="source language")
    dst_lang = models.CharField(max_length=255, verbose_name='destination language')
    pdf = models.FileField(upload_to='pdfs/',verbose_name="pdf")
    pdf_name = models.CharField(max_length=1255 , verbose_name="pdf file name")
    md = models.FileField(null=True,blank=True,upload_to='mds/' , verbose_name="markdown file")
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True , verbose_name="created_at")
    model_name = models.CharField(choices=[("4o-mini","4o-mini"),("3-turbo","3-turbo")],verbose_name="model_name", null=True)