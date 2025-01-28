from django.shortcuts import render,redirect
import documents
from .forms import TaskPerson_in,Partner_in,Parent_in,Dead_in
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Person,Marrid,Dead,Divorce,TaskPerson,Widower
from documents.models import Document
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.core.mail import BadHeaderError
import smtplib
import csv

def move_person(tasked_person):
    new_object_data = {
        'person_name' : tasked_person.person_name,
        'national_num' : tasked_person.national_num,
        'first_name' : tasked_person.first_name,
        'last_name' : tasked_person.last_name,
        'dad_name' : tasked_person.dad_name,
        'national_dad' : tasked_person.national_dad,
        'mom_name' : tasked_person.mom_name,
        'national_mom' : tasked_person.national_mom,
        'birth_place' : tasked_person.birth_place,
        'birth_date' : tasked_person.birth_date,
        'date_of_issue' : tasked_person.date_of_issue,
        'place_of_issue' : tasked_person.place_of_issue,
        'number_of_issue' : tasked_person.number_of_issue,
        'religion' : tasked_person.religion,
        'gender' : tasked_person.gender,
        'status' : tasked_person.status,
        'image' : tasked_person.image,
        }
    person = Person.objects.create(**new_object_data)
    return person

def move_tasked_person(tasked_person):
    new_object_data = {
        'person_name' : tasked_person.person_name,
        'national_num' : tasked_person.national_num,
        'first_name' : tasked_person.first_name,
        'last_name' : tasked_person.last_name,
        'dad_name' : tasked_person.dad_name,
        'national_dad' : tasked_person.national_dad,
        'mom_name' : tasked_person.mom_name,
        'national_mom' : tasked_person.national_mom,
        'birth_place' : tasked_person.birth_place,
        'birth_date' : tasked_person.birth_date,
        'date_of_issue' : tasked_person.date_of_issue,
        'place_of_issue' : tasked_person.place_of_issue,
        'number_of_issue' : tasked_person.number_of_issue,
        'religion' : tasked_person.religion,
        'gender' : tasked_person.gender,
        'status' : tasked_person.status,
        'image' : tasked_person.image,
        }
    person = TaskPerson.objects.create(**new_object_data)
    return person

def person_is_here(request):

        page_name = 'person who not in the data base'
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists() :
            return redirect('users:main')
        else:
            if TaskPerson.objects.filter(person_name=name).exists() :
                person = TaskPerson.objects.filter(person_name=name).last()
                choices = ['add personal information','show new documents','pay for orders','show payments']
                return render(request,'pages/main_new.html',{'emperson':person,'choices':choices,'page_name':page_name})
            else:
                return redirect('users:add_person_information')



def add_person_information(request):
        user_is_logined(request)
        person_name=user_is_logined(request)
        error=' '
        task_name = 'add information'
        if request.method == "POST":
            data = TaskPerson_in(request.POST,request.FILES)
            if data.is_valid():
                national_num = request.POST['national_num']
                data.save()
                person_s = TaskPerson.objects.get(national_num = national_num,code=None)
                person_s.person_name = person_name
                person_s.save()
                request.session['task_name'] = task_name
                code = documents.views.insert_task_code(request)
                person_s.code = code
                person_s.save()
                request.session['document_code'] = code
                return redirect('users:person_is_here')
            else:
                error = data.errors
        if Person.objects.filter(person_name=person_name).exists():
            person = Person.objects.get(person_name=person_name)
            return render(request,'users/person_in.html',{'emperson':person,'person':TaskPerson_in,'error':error,'task_name':task_name})
        else :
            return render(request,'users/person_in_new.html',{'person':TaskPerson_in,'error':error,'task_name':task_name})

def person_in(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        error=' '
        task_name = 'add person'
        if request.method == "POST":
            data = TaskPerson_in(request.POST,request.FILES)
            if data.is_valid():
                national_num = request.POST['national_num']
                data.save()
                Person_s = TaskPerson.objects.get(national_num = national_num,code=None)
                national_num = Person_s.national_num
                request.session['task_name'] = task_name
                request.session['second_national_num'] = national_num
                code = documents.views.insert_task_code(request)
                Person_s.code = code
                Person_s.save()
                request.session['document_code'] = code
                return redirect('users:main')
            else:
                error = data.errors
        return render(request,'users/person_in.html',{'emperson':person,'person':TaskPerson_in,'error':error,'task_name':task_name})



def person_save(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        error=' '
        task_name = 'save person'
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        second_national_num = document.second_national_num
        if Person.objects.filter(national_num=second_national_num).exists():
            person_added_exist = Person.objects.get(national_num=second_national_num)
            person_name = person_added_exist.person_name
            if person_name != None :
                error = 'the asked person can not modify'
        else :
             person_name = 'No one'
        tasked_person_added = TaskPerson.objects.get(code=document_code)
        if request.method == "POST":
            if person_name == None :
                person_added_exist.delete()
            person_added = move_person(tasked_person_added)
            person_added.save()
            tasked_person_added.delete()
            document.done = True
            document.save()
            error = 'the person had been saved succefully'
        return render(request,'users/person_save.html',{'emperson':person,'person':tasked_person_added,'error':error,'task_name':task_name})



def information_save(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        error=' '
        task_name = 'save person information'
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        person_national_num = document.person_national_num
        tasked_person_added = TaskPerson.objects.get(code=document_code)
        tasked_person_added_name =tasked_person_added.person_name
        if request.method == "POST":
            if Person.objects.filter(national_num=person_national_num).exists():
                past_person = Person.objects.get(national_num=person_national_num)
                past_person.delete()
            if Person.objects.filter(person_name=tasked_person_added_name).exists():
                past_person = Person.objects.get(person_name=tasked_person_added_name)
                past_person.delete()
            person_added = move_person(tasked_person_added)
            person_added.save()
            tasked_person_added.delete()
            document.done = True
            document.save()
            error = _("Data saved successfully!")
        return render(request,'users/person_save.html',{'emperson':person,'person':tasked_person_added,'error':error,'task_name':task_name})



def get_by_obj(national_num):
    if Person.objects.filter(national_num = national_num).exists() :
        user = Person.objects.get(national_num = national_num)
    else :
        user = Person.objects.get(national_num = '00000000000')
    return user

def user_is_logined(request):
    if request.user.is_authenticated:
        name = request.user.username
        return name
    else :
        return redirect ('registering:CustomLoginView')

def get_marrid(person):
    marrid_partner=[]
    if person.gender == 'male':
        partners = Marrid.objects.filter(national_hus=person.national_num)
        if len(partners) !=0:
            for partner in partners :
                marrid_partner.append(Person.objects.get(national_num=partner.national_wife))
    else :
        partners = Marrid.objects.filter(national_wife=person.national_num)
        if len(partners) !=0:
            for partner in partners :
                marrid_partner.append(Person.objects.get(national_num=partner.national_hus))
    return marrid_partner

def get_divorce(person):
    divorce_partner=[]
    if person.gender == 'male':
        partners = Divorce.objects.filter(national_hus=person.national_num)
        if len(partners) !=0:
            for partner in partners :
                divorce_partner.append(Person.objects.get(national_num=partner.national_wife))
        else :
            partners = Divorce.objects.filter(national_wife=person.national_num)
            if len(partners) !=0:
                for partner in partners :
                    divorce_partner.append(Person.objects.get(national_num=partner.national_hus))
    return divorce_partner

def get_family(national_num):
    family = []
    person = Person.objects.get(national_num=national_num)
    if person.gender == 'male':
        family.append(person)
        family_member = Person.objects.filter(national_dad=person.national_num)

    marrid_member = get_marrid(person)
    for user in marrid_member :
        family.append(user)

    if person.gender != 'male':
        family.append(person)
        family_member = Person.objects.filter(national_mom=person.national_num)

    for user in family_member :
        family.append(user)

    return family

def person_show(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        task_name = 'birth register'
        request.session['task_name'] = task_name
        return render(request,'users/person_in.html',{'emperson':person,'person':person,'task_name':task_name})



def main(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        page_name = _("main")
        if Person.objects.get(person_name=name).is_employee:
            choices = ['show documents','enter payment']
        else:
            choices = ["choose document",'assert information','show documents','pay for orders','show payments']
        return render(request,'pages/main.html',{'emperson':person,'person':person,'choices':choices,'page_name':page_name})


def assert_information(request):
    name = user_is_logined(request=request)
    if Person.objects.filter(person_name=name).exists():
        person = Person.objects.filter(person_name=name)
    else :
        return redirect ('users:add_person_information')
    page_name = 'assert_information'
    choices = ['add personal information','add person','add parent','add event','add partner','add died person','death record']
    return render(request,'pages/main.html',{'emperson':person,'person':person,'choices':choices,'page_name':page_name})

def get_choice(request):

        if request.method == 'POST':
            name = request.POST.get('name')
            choices = {
                'show new documents':'../documents/show_new_documents',
                'choose document':'../documents/choose_document',
                'assert information':'assert_information',
                'show documents':'../documents/show_documents',
                'pay for orders':'../payment/orders' ,
                'show payments': '../payment/view_payments',
                'enter payment':'../payment/enter_payment_amount',
                'add personal information':'add_person_information',
                'add person':'person_in',
                'add parent':'parent_in',
                'add event':'event_in',
                'add partner':'partner_in',
                'add died person':'died_person_record',
                'death record':'death_record'
            }
            path = choices [name]
            url = f'{path}'
            return JsonResponse({'status': 'redirect', 'url': url})
        return JsonResponse({'status': 'fail'}, status=400)



def parent_in(request):
        person_name = user_is_logined(request=request)
        if Person.objects.filter(person_name=person_name).exists():
            person = Person.objects.get(person_name=person_name)
        else :
            return redirect ('users:person_is_here')
        error=' '
        task_name = 'add parent'
        if request.method == "POST":
            data = Parent_in(request.POST,request.FILES)
            if data.is_valid():
                national_parent_num = request.POST['national_parent_num']
                gender_parent = request.POST['gender_parent']
                first_name = request.POST['first_parent_name']
                last_name = request.POST['last_parent_name']
                image = data.cleaned_data['image']
                data_f = TaskPerson(first_name=first_name,last_name=last_name,national_num=national_parent_num,gender=gender_parent)#image=image
                request.session['task_name'] = task_name
                request.session['second_national_num'] = national_parent_num
                code = documents.views.insert_task_code(request)
                data_f.code = code
                data_f.save()
                return redirect('users:main')
            else:
                error = data.errors
        return render(request,'users/parent.html',{'emperson':person,'person':person,'parent':Parent_in,'error':error,'person_name':person_name,'task_name':task_name})



def parent_save(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        tasked_person = documents.views.get_person(request)
        error=' '
        task_name = 'save parent'
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        person_national_num = document.person_national_num
        parent_national_num = document.second_national_num
        tasked_parent = TaskPerson.objects.get(code=document_code)
        if request.method == "POST":
            person_exist = Person.objects.filter(national_num=person_national_num).exists()
            parent_exist = Person.objects.filter(national_num = parent_national_num).exists()
            if person_exist :
                person = Person.objects.get(national_num=person_national_num)
                if tasked_parent.gender =='male':
                    person.national_dad = parent_national_num
                else :
                    person.national_mom = parent_national_num
                person.save()
                if not parent_exist :
                    parent = move_person(tasked_parent)
                    parent.save()
                    tasked_parent.delete()
                    document.done = True
                    document.save()
                    error = "Data saved successfully!"
                else :
                    error = 'there\'s a person with this national id , just him can modify his informations'
            else :
                error = 'the person who asked not inserted his informations'
        return render(request,'users/person_save.html',{'emperson':person,'person':tasked_parent,'error':error,'task_name':task_name})



def index(request):

        dex = ''
        file = open("test.csv")
        csvreader = csv.reader(file)
        for row in csvreader:
            ex  = Person.objects.filter(person_name=row[0])
            if len(ex) == 0:
                person = Person(person_name=row[0],national_num=row[1],first_name=row[2],last_name=row[3],national_dad=row[4],
                national_mom=row[5],birth_place=row[6],birth_date=row[7],date_of_issue=row[8],place_of_issue=row[9],
                number_of_issue=row[10],status=row[11],religion=row[12],gender=row[13],)
                person.save()
                dex = 'done'
            else :
                dex = 'they are in'
        file.close()
        return render(request,'pages/pages.html',{'dex':dex})



def event_in(request):
        person_name = user_is_logined(request=request)
        if Person.objects.filter(person_name=person_name).exists():
            person = Person.objects.get(person_name=person_name)
        else :
            return redirect ('users:person_is_here')
        error = ''
        task_name = 'add event'
        if request.method == "POST" :
            data = Partner_in(request.POST,request.FILES)
            if data.is_valid() :
                partner_national_num = request.POST['partner_national_num']
                date_of_event = request.POST['date_of_event']
                marrid = request.POST['marrid']
                image = data.cleaned_data['image']
                request.session['second_national_num'] = partner_national_num
                if marrid == 'marrid':
                    task_name = 'add marrid'
                if marrid == 'divorce':
                    task_name = 'add divorce'
                if marrid == 'widower':
                    task_name = 'add widower'
                person = Person.objects.get(person_name=person_name)
                if Person.objects.filter(national_num=partner_national_num).exists() :
                    partner = Person.objects.get(national_num=partner_national_num)
                    partner = move_tasked_person(partner)
                    if person.gender == partner.gender:
                        error ="can't be a partner"
                    else :
                        request.session['task_name'] = task_name
                        code = documents.views.insert_task_code(request)
                        partner.code = code
                        partner.date_of_event = date_of_event
                        partner.image = image
                        partner.save()
                        del request.session['document_code']
                        return redirect('users:main')
                else :
                    error = 'please assert a person first'
            else:
                error = data.errors
        return render(request,'users/partner.html',{'emperson':person,'event':Partner_in,'error':error,'person_name':person_name,'task_name':task_name})



def partner_in(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        error = ''
        task_name = 'add partner'
        person_name = name
        if request.method == "POST" :
            data = TaskPerson_in(request.POST,request.FILES)
            if data.is_valid() :
                partner_national_num = request.POST['national_num']
                data.save()
                tasked_partner = TaskPerson.objects.get(national_num = partner_national_num,code=None)
                marrid = tasked_partner.status
                request.session['second_national_num'] = partner_national_num
                if marrid == 'married':
                    task_name = 'add marrid'
                if marrid == 'divorce':
                    task_name = 'add divorce'
                if marrid == 'widower':
                    task_name = 'add widower'
                if marrid == 'single':
                    task_name = 'add person'
                request.session['task_name'] = task_name
                person = Person.objects.get(person_name=person_name)
                if Person.objects.filter(national_num=partner_national_num).exists() :
                    error = 'there is a person who must modify hus informations'
                else :
                    if person.gender == tasked_partner.gender:
                        error ="can't be a partner"
                    else :
                        code = documents.views.insert_task_code(request)
                        request.session['document_code'] = code
                        tasked_partner.code = code
                        tasked_partner.save()
                        del request.session['document_code']
                        return redirect('users:main')
            else:
                error = data.errors
        return render(request,'users/partner_in.html',{'emperson':person,'person':TaskPerson_in,'error':error,'person_name':person_name,'task_name':task_name})



def add_marrid(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        tasked_person = documents.views.get_person(request)
        tasked_person_name = tasked_person.person_name
        error=' '
        task_name = 'save marrid'
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        person_national_num = document.person_national_num
        partner_national_num = document.second_national_num
        person_exist = Person.objects.filter(national_num=person_national_num).exists()
        partner_exist = Person.objects.filter(national_num = partner_national_num).exists()
        tasked_partner = TaskPerson.objects.get(code=document_code)
        date_of_event = tasked_partner.date_of_event
        image = tasked_partner.image
        if request.method == "POST":
            if person_exist :
                person = Person.objects.get(national_num=person_national_num)
                person.status = 'marrid'
                person.save()
                if not partner_exist :
                    partner_save = move_person(tasked_partner)
                    partner_save.save()
                partner = Person.objects.get(national_num=partner_national_num)
                if person.gender == 'male':
                    national_hus = person.national_num
                    national_wife = partner.national_num
                else :
                    national_wife = person.national_num
                    national_hus = partner.national_num
                relation = Marrid(national_hus=national_hus,national_wife=national_wife,date_of_event=date_of_event,image=image)
                relation.save()
                tasked_partner.delete()
                document.done = True
                document.save()
                error = 'the person had been saved succefully'
            else :
                error = 'the person who asked not inserted his informations'
        return render(request,'users/partner_save.html',{'emperson':person,'person':partner,'error':error,'task_name':task_name})



def add_divorce(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        tasked_person = documents.views.get_person(request)
        tasked_person_name = tasked_person.person_name
        error=' '
        task_name = 'save divorce'
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        person_national_num = document.person_national_num
        partner_national_num = document.second_national_num
        person_exist = Person.objects.filter(national_num=person_national_num).exists()
        partner_exist = Person.objects.filter(national_num = partner_national_num).exists()
        tasked_partner = TaskPerson.objects.get(code=document_code)
        date_of_event = tasked_partner.date_of_event
        image = tasked_partner.image
        if person_exist :
            person = Person.objects.get(national_num=person_national_num)
            if not partner_exist :
                partner_save = move_person(tasked_partner)
                partner_save.save()
            partner = Person.objects.get(national_num=partner_national_num)
            if person.gender == 'male':
                national_hus = person.national_num
                national_wife = partner.national_num
            else :
                national_wife = person.national_num
                national_hus = partner.national_num
            if Marrid.objects.filter(national_hus=national_hus,national_wife=national_wife).exists():
                Marrid.objects.filter(national_hus=national_hus,national_wife=national_wife).delete()
            relation = Divorce(national_hus=national_hus,national_wife=national_wife,date_of_event=date_of_event,image=image)
            relation.save()
            tasked_partner.delete()
            document.done = True
            document.save()
            error = 'the person had been saved succefully'
        else :
            error = 'the person who asked not inserted his informations'
        return render(request,'users/partner_save.html',{'emperson':person,'person':partner,'error':error,'task_name':task_name})



def add_widower(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        tasked_person = documents.views.get_person(request)
        tasked_person_name = tasked_person.person_name
        error=' '
        task_name = 'save widower'
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        person_national_num = document.person_national_num
        partner_national_num = document.second_national_num
        person_exist = Person.objects.filter(national_num=person_national_num).exists()
        partner_exist = Person.objects.filter(national_num = partner_national_num).exists()
        tasked_partner = TaskPerson.objects.get(code=document_code)
        date_of_widower = tasked_partner.date_of_event
        image = tasked_partner.image
        if request.method == "POST":
            if person_exist :
                person = Person.objects.get(national_num=person_national_num)
                if not partner_exist :
                    partner_save = move_person(tasked_partner)
                    partner_save.save()
                partner = Person.objects.get(national_num=partner_national_num)
                if person.gender == 'male':
                    national_hus = person.national_num
                    national_wife = partner.national_num
                else :
                    national_wife = person.national_num
                    national_hus = partner.national_num
                relation = Widower(national_hus=national_hus,national_wife=national_wife,date_of_widower=date_of_widower,image=image)
                relation.save()
                tasked_partner.delete()
                document.done = True
                document.save()
                error = "Data saved successfully!"
            else :
                error = 'the person who asked not inserted his informations'
        return render(request,'users/partner_save.html',{'emperson':person,'person':partner,'error':error,'task_name':task_name})



def get_first_relation(person):
    first_relation = []
    for x in Person.objects.filter(national_num=person.national_dad):
        first_relation.append(x)
    for x in Person.objects.filter(national_num=person.national_mom):
        first_relation.append(x)
    for x in Person.objects.filter(national_dad=person.national_dad):
        first_relation.append(x)
    for x in Person.objects.filter(national_mom=person.national_mom):
        first_relation.append(x)
    for x in Person.objects.filter(national_dad=person.national_num):
        first_relation.append(x)
    for x in Person.objects.filter(national_mom=person.national_num):
        first_relation.append(x)
    for partner in get_marrid(person) :
        first_relation.append(partner)
    return first_relation

def death_record(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        person = Person.objects.get(person_name=name)
        error=' '
        task_name = 'death record'
        if request.method == "POST":
            data = Dead_in(request.POST,request.FILES)
            if data.is_valid():
                national_num = request.POST['national_num']
                place_of_death = request.POST['place_of_event']
                date_of_event = request.POST['date_of_event']
                image = data.cleaned_data['image']
                if Person.objects.filter(national_num=national_num).exists(): # type: ignore
                    dead_person = Person.objects.get(national_num=national_num) # type: ignore
                    tasked_dead_person = move_tasked_person(dead_person)
                    first_relation = get_first_relation(tasked_dead_person)
                    if person in first_relation :
                        request.session['second_national_num'] = national_num
                        request.session['task_name'] = task_name
                        code = documents.views.insert_task_code(request)
                        tasked_dead_person.code = code
                        tasked_dead_person.place_of_event = place_of_death
                        tasked_dead_person.date_of_event = date_of_event
                        tasked_dead_person.image = image
                        tasked_dead_person.save()
                        request.session['document_code'] = code
                        return redirect('users:main')
                    else :
                        error = _("The applicant does not have the right to access the data of the dead person")
                else :
                    error = 'please assert a person first'
            else:
                error = data.errors
        return render(request,'users/died_person.html',{'emperson':person,'died':Dead_in,'error':error,'person_name':name,'task_name':task_name})



def died_person_record(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        error = ''
        task_name = 'death record'
        person_name = name
        if request.method == "POST" :
            data = TaskPerson_in(request.POST,request.FILES)
            if data.is_valid() :
                dead_national_num = request.POST['national_num']
                data.save()
                tasked_dead = TaskPerson.objects.get(national_num = dead_national_num,code=None)
                request.session['second_national_num'] = dead_national_num
                request.session['task_name'] = 'death record'
                person = Person.objects.get(person_name=person_name)
                if Person.objects.filter(national_num=dead_national_num).exists() :
                    error ='thre is a person please go to death record'
                else :
                    first_relation = get_first_relation(tasked_dead)
                    if person in first_relation :
                        code = documents.views.insert_task_code(request)
                        request.session['document_code'] = code
                        tasked_dead.code = code
                        tasked_dead.save()
                        del request.session['document_code']
                        return redirect('users:main')
                    else :
                        error = "you can't record this dead person"
            else:
                error = data.errors
        return render(request,'users/partner_in.html',{'emperson':person,'person':TaskPerson_in,'error':error,'person_name':person_name,'task_name':task_name})



def death_save(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        tasked_person = documents.views.get_person(request)
        tasked_person_name = tasked_person.person_name
        error=' '
        task_name = 'death save'
        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        person_national_num = document.person_national_num
        dead_national_num = document.second_national_num
        person_exist = Person.objects.filter(national_num=person_national_num).exists()
        dead_exist = Person.objects.filter(national_num = dead_national_num).exists()
        tasked_dead = TaskPerson.objects.get(code=document_code)
        date_of_event = tasked_dead.date_of_event
        place_of_death = tasked_dead.place_of_event
        image = tasked_dead.image
        if request.method == "POST":
            if person_exist :
                person = Person.objects.get(national_num=person_national_num)
                first_relation = get_first_relation(tasked_dead)
                if person in first_relation :
                    if not dead_exist :
                        dead_save = move_person(tasked_dead)
                        dead_save.save()
                    dead = Person.objects.get(national_num=dead_national_num)
                    marriages = Marrid.objects.filter(national_hus=dead_national_num)
                    for mariage in marriages:
                        mariage.delete()
                    if Marrid.objects.filter(national_wife=dead_national_num):
                        Marrid.objects.filter(national_wife=dead_national_num).delete()
                    relation = Dead(national_num=dead_national_num,date_of_event=date_of_event,place_of_death=place_of_death,image=image)
                    relation.save()
                    tasked_dead.delete()
                    document.done = True
                    document.save()
                    error = 'the person had been saved succefully'
                else :
                    error = "there\'re no relation between the person and the dead person"
            else :
                error = 'the person who asked not inserted his informations'
        return render(request,'users/partner_save.html',{'emperson':person,'person':tasked_dead,'error':error,'task_name':task_name})


def about(request):
    return render(request,"pages/about.html")

