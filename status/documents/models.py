from django.db import models
from datetime import datetime

class Document(models.Model):
    name = models.CharField(max_length=15)
    code = models.CharField(max_length=15)
    person_national_num = models.CharField(max_length=15)
    second_national_num = models.CharField(max_length=15,null=True,blank=True)
    document_date = models.DateTimeField(default=datetime.now)
    viewed = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    paid = models.CharField(max_length=15,default='not paid')
    notes = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    
