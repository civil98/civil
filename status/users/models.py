from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    gender_person=[
        ('male','Male'),
        ('female','Female')
    ]
    status_person=[
        ('single','single'),
        ('married','married'),
        ('divorced','divorced'),
        ('widower','widower')
    ]
    religion_person=[
        ('muslim','muslim'),
        ('Christian','Christian')
    ]
    person_name = models.CharField(max_length=15,unique=True,null=True)
    national_num = models.CharField(max_length=15,unique=True)
    first_name = models.CharField(max_length=15,null=True)
    last_name = models.CharField(max_length=15,null=True)
    dad_name = models.CharField(max_length=15,null=True)
    national_dad = models.CharField(max_length=15,null=True)
    mom_name = models.CharField(max_length=15,null=True)
    national_mom = models.CharField(max_length=15,null=True)
    birth_place = models.CharField(max_length=15,null=True)
    birth_date = models.DateField(null=True)
    date_of_issue = models.DateField(null=True)
    place_of_issue =models.CharField(max_length=15,null=True)
    number_of_issue = models.IntegerField(null=True)
    religion = models.CharField(max_length=9,choices=religion_person,default='muslim')
    gender = models.CharField(max_length=7,choices=gender_person,default='male')
    status = models.CharField(max_length=8,choices=status_person,default='single')
    is_employee = models.BooleanField(default=False)
    image = models.ImageField(upload_to='image/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.national_num
    

class TaskPerson(models.Model):
    gender_person=[
        ('male','Male'),
        ('female','Female')
    ]
    status_person=[
        ('single','single'),
        ('married','married'),
        ('divorced','divorced'),
        ('widower','widower')
    ]
    religion_person=[
        ('muslim','muslim'),
        ('Christian','Christian')
    ]
    person_name = models.CharField(max_length=15,null=True)
    national_num = models.CharField(max_length=15)
    first_name = models.CharField(max_length=15,null=True)
    last_name = models.CharField(max_length=15,null=True)
    dad_name = models.CharField(max_length=15,null=True)
    national_dad = models.CharField(max_length=15,blank=True,null=True)
    mom_name = models.CharField(max_length=15,null=True)
    national_mom = models.CharField(max_length=15,blank=True,null=True)
    birth_place = models.CharField(max_length=15,null=True)
    birth_date = models.DateField(null=True)
    date_of_issue = models.DateField(null=True)
    place_of_issue =models.CharField(max_length=15,null=True)
    number_of_issue = models.IntegerField(null=True)
    religion = models.CharField(max_length=9,choices=religion_person,default='muslim')
    gender = models.CharField(max_length=7,choices=gender_person,default='male')
    status = models.CharField(max_length=8,choices=status_person,default='single')
    image = models.ImageField(upload_to='image/%y/%m/%d', blank=True, null=True)
    date_of_event = models.DateField(blank=True, null=True)
    place_of_event =models.CharField(max_length=15,blank=True, null=True)
    code = models.CharField(max_length=15,null=True)
    
    def __str__(self):
        return self.national_num


class Marrid(models.Model):
    national_hus = models.CharField(max_length=15)
    national_wife = models.CharField(max_length=15,unique=True)
    date_of_event = models.DateField(null=True)
    place_of_event =models.CharField(max_length=15,null=True)
    image = models.ImageField(upload_to='image/%y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return self.national_hus


class Divorce(models.Model):
    national_hus = models.CharField(max_length=15)
    national_wife = models.CharField(max_length=15)
    date_of_event = models.DateField(null=True)
    place_of_event =models.CharField(max_length=15,null=True)
    image = models.ImageField(upload_to='image/%y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return self.national_hus


class Widower(models.Model):
    national_hus = models.CharField(max_length=15)
    national_wife = models.CharField(max_length=15)
    date_of_divorce = models.DateField(null=True)
    image = models.ImageField(upload_to='image/%y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return self.national_hus


class Dead(models.Model):
    national_num = models.CharField(max_length=15)
    date_of_event = models.DateField(null=True)
    place_of_event =models.CharField(max_length=15,null=True)
    image = models.ImageField(upload_to='image/%y/%m/%d', blank=True, null=True)
    
    def __str__(self):
        return self.national_num
