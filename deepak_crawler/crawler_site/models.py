from django.db import models
from django import forms
# Create your models here.
class QueryForm(forms.Form):
    query = forms.CharField(label='query',max_length=100)

class Authors(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    pfp_link = models.CharField(max_length=1000)
    email = models.CharField(max_length=100, default="N\A")
    affiliation = models.CharField(max_length=1000, default="N\A")
    citations = models.CharField(max_length=1000, default="N\A")