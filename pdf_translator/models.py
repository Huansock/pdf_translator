from django.db import models
# Create your models here.
class Translator (models.Model):
    id = models.AutoField(blank=True,primary_key=True)
    src_lang = models.CharField(max_length=255)
    dst_lang = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdfs/')
    pdf_name = models.CharField(max_length=1255)
    md = models.FileField(null=True,blank=True,upload_to='mds/')
    created_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)