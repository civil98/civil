from django.shortcuts import render,redirect
from users.views import get_family,get_marrid,get_first_relation,user_is_logined,get_divorce,main,person_is_here
from users.models import Person,Marrid,Divorce,Dead,TaskPerson
from .forms import Death_register,Send_notes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from payment.models import Order
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def send_email_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient_list = [request.POST.get('email')]

        try:
            print('1')
            print(settings.DEFAULT_FROM_EMAIL)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            messages.success(request, 'تم إرسال البريد الإلكتروني بنجاح!')
            return redirect('family_doc')  # استبدلها بالعنوان URL المطلوب
        except Exception as e:
            er = messages.error(request, f'حدث خطأ: {e}')
            print(er)

    return render(request, 'mail/mail.html')

def get_person(request):
        name = user_is_logined(request=request)
        try :
            document_code = request.session.get('document_code','0')
            document = Document.objects.get(code=document_code)
            person_national_num =document.person_national_num
            if Person.objects.filter(national_num=person_national_num).exists() :
                person = Person.objects.get(national_num=person_national_num)
            elif TaskPerson.objects.filter(national_num=person_national_num).exists() :
                person = TaskPerson.objects.get(national_num=person_national_num,code=None)
        except:
            if Person.objects.filter(person_name=name).exists() :
                person = Person.objects.get(person_name=name)
            elif TaskPerson.objects.filter(person_name=name).exists() :
                person = TaskPerson.objects.get(person_name=name,code=None)
        return person

def refuse_with_note(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        error = ''
        task_name = 'refuse with note'
        if request.method == "POST":
            data = Send_notes(request.POST)
            if data.is_valid():
                notes = request.POST['notes']
                code = request.session.get('document_code','0')
                document = Document.objects.get(code=code)
                document_notes = document.notes
                notes = notes + '\n' + name + '   ' + str(datetime.now()) + '\n'
                document_notes = document_notes + notes
                document.notes = document_notes
                document.document_date = str(datetime.now())
                document.viewed = True
                document.save()
                return redirect('documents:show_documents')
            else :
                error = data.errors
        return render(request,'documents/note.html',{'emperson':person,'form':Send_notes,'error':error,'task_name':task_name})

def send_notes(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        elif TaskPerson.objects.filter(person_name=name).exists():
            person = TaskPerson.objects.filter(person_name=name).last()
        else :
            return redirect ('users:person_is_here')
        error = ''
        task_name = 'add note'
        if request.method == "POST":
            data = Send_notes(request.POST)
            if data.is_valid():
                notes = request.POST['notes']
                code = request.session.get('document_code','0')
                document = Document.objects.get(code=code)
                document_notes = document.notes
                notes = notes + '\n' + name + '   ' + str(datetime.now()) + '\n'
                document_notes = document_notes + notes
                document.notes = document_notes
                document.document_date = str(datetime.now())
                document.viewed = False
                document.save()
                messages.success(request, _("Data saved successfully!"))
                return redirect('documents:review_task')
            else :
                error = data.errors
        return render(request,'documents/note.html',{'emperson':person,'form':Send_notes,'error':error,'task_name':task_name})

def family_register(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        person = get_person(request=request)
        employee = person
        task_name = 'family register'
        event = False
        if person.status == 'single':
            national_num = person.national_dad
            try :
                person = Person.objects.get(national_num = national_num)
            except:
                 return HttpResponse('please assert your dad first to get family register')
        national_num = person.national_num
        family = get_family(national_num=national_num)
        request.session['task_name'] = task_name
        return render(request,'documents/confirm_family.html',{'emperson':emperson,'person':person,'family':family,'task_name':task_name,'event':event,'employee':employee})


def birth_register(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        person = get_person(request=request)
        task_name = 'birth register'
        event = False
        request.session['task_name'] = task_name
        employee = person
        return render(request,'documents/confirm_person.html',{'emperson':emperson,'person':person,'task_name':task_name,'event':event,'employee':employee})



def show_marriage_register(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        family = []
        person = get_person(request=request)
        national_num = request.GET.get('national_num')
        if national_num is None :
            code = request.session.get('document_code','0')
            document = Document.objects.get(code=code)
            national_num = document.second_national_num
        partner_national_num = national_num
        partner = Person.objects.get(national_num=partner_national_num)
        if person.gender == 'male':
            husband = person
            wife = partner
        else :
            husband = person
            wife = partner
        if partner in get_marrid(person):
            task_name = 'marriage'
            request.session['task_name'] = 'marriage register'
            event = Marrid.objects.get(national_wife=wife.national_num)
        if partner in get_divorce(person):
            task_name = 'divorce'
            divorce_times = Divorce.objects.filter(national_wife=wife.national_num)
            request.session['task_name'] = 'divorce register'
            for time in divorce_times :
                if time.national_hus == person.national_num :
                    event = time
        family.append(husband)
        family.append(wife)
        request.session['second_national_num'] = wife.national_num
        employee = person
        return render(request,'documents/confirm_family.html',{'emperson':emperson,'person':person,'family':family,'task_name':task_name,'event':event,'employee':employee})



def marriage_register(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        person = get_person(request=request)
        family = []
        if person.gender == 'male':
            task_name = 'all marriage'
        marrid_member = get_marrid(person)
        for user in marrid_member :
            family.append(user)
        if person.gender == 'female':
            task_name = 'marriage register'
        return render(request,'documents/show_all.html',{'emperson':emperson,'person':person,'family':family,'task_name':task_name})



def divorce_register(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        person = get_person(request=request)
        divorce_group = []
        if person.gender == 'male':
            task_name = 'divorce all'
        divorce_member = get_divorce(person)
        for user in divorce_member :
            divorce_group.append(user)
        if person.gender == 'female':
            task_name = 'divorce register'
        request.session['task_name'] = 'divorce register'
        return render(request,'documents/show_all.html',{'emperson':emperson,'person':person,'family':divorce_group,'task_name':task_name})



def death_register_show(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        person = get_person(request=request)
        person_name =person.person_name
        task_name = 'death register'
        code = request.session.get('document_code','0')
        document = Document.objects.get(code=code)
        national_dead = document.second_national_num
        if Dead.objects.filter(national_num=national_dead).exists():
            if Person.objects.filter(national_num=national_dead).exists():
                dead_person = Person.objects.get(national_num=national_dead)
                first_relation = get_first_relation(person)
                if dead_person in first_relation :
                    family =[]
                    family.append(dead_person)
                    event = Dead.objects.get(national_num=national_dead)
                    request.session['task_name'] = task_name
                    employee = person
                else :
                    error = "The applicant does not have the right to access the data of the dead person"
            else :
                error = "No one has this national number"
        else :
            error = _("there's no one dead with this national number")
        return render(request,'documents/confirm_person.html',{'emperson':emperson,'person':person,'task_name':task_name,'person_name':person_name,'error':error,'event':event,'employee':employee})



def death_register(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        person = get_person(request=request)
        person_name =person.person_name
        error=' '
        task_name = 'death register'
        if request.method == "POST":
            data = Death_register(request.POST)
            if data.is_valid():
                national_dead = request.POST['national_dead']
                if Dead.objects.filter(national_num=national_dead).exists():
                    if Person.objects.filter(national_num=national_dead).exists():
                        dead_person = Person.objects.get(national_num=national_dead)
                        first_relation = get_first_relation(person)
                        if dead_person in first_relation :
                            family =[]
                            family.append(dead_person)
                            event = Dead.objects.get(national_num=national_dead)
                            request.session['task_name'] = task_name
                            employee = person
                            return render(request,'documents/confirm_person.html',{'person':person,'task_name':task_name,'person_name':person_name,'event':event,'employee':employee})
                        else :
                            error = "The applicant does not have the right to access the data of the dead person"
                    else :
                        error = "No one has this national number"
                else :
                    error = "there's no one dead with this national number"
        return render(request,'documents/note.html',{'emperson':emperson,'form':Death_register,'error':error,'task_name':task_name})

def delete_document(request):
    document_code = request.session.get('document_code','0')
    document = Document.objects.get(code=document_code)
    if TaskPerson.objects.filter(code=document_code).exists():
        TaskPerson.objects.get(code=document_code).delete()
    document.delete()
    del request.session['document_code']
    name = user_is_logined(request=request)
    if Person.objects.filter(person_name=name).exists():
        return redirect('documents:show_documents')
    else :
        return redirect('documents:show_new_documents')


def choose_document(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        task_name = 'choose document'
        documents = ['family register','birth register','marriage register','divorce register','death register']
        return render(request,'documents/choose_document.html',{'emperson':emperson,'documents':documents,'task_name':task_name})



def get_document(request):

        if request.method == 'POST':
            name = request.POST.get('name')
            documents = {
                'family register' : 'family_register',
                'birth register' : 'birth_register',
                'marriage register' : 'marriage_register',
                'divorce register' : 'divorce_register',
                'death register' : 'death_register'
            }
            name = documents[name]
            url = f'{name}'
            return JsonResponse({'status': 'redirect', 'url': url})
        return JsonResponse({'status': 'fail'}, status=400)



def review_task(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        elif TaskPerson.objects.filter(person_name=name).exists():
            person = TaskPerson.objects.filter(person_name=name).last()
        else :
            return redirect ('users:person_is_here')
        code = request.GET.get('code')
        if  code == None :
            code = request.session.get('document_code','0')
        else :
            request.session['document_code'] = code
        document = Document.objects.get(code=code)
        task_name = document.name
        return render(request,'documents/review_task.html',{'emperson':person,'document':document,'task_name':task_name,'person':person})



def show_documents(request):
        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            person = Person.objects.get(person_name=name)
        else :
            return redirect ('users:person_is_here')
        task_name = 'show documents'
        documents = []
        if person.is_employee:
            documents = Document.objects.filter(viewed=False,done=False,paid='paid')
        else :
            documents = Document.objects.filter(person_national_num=person.national_num)
        return render(request,'documents/show_documents.html',{'emperson':person,'documents':documents,'task_name':task_name})



def show_new_documents(request):

        name = user_is_logined(request=request)
        if Person.objects.filter(person_name=name).exists():
            emperson = Person.objects.get(person_name=name)
        elif TaskPerson.objects.filter(person_name=name).exists():
            emperson = TaskPerson.objects.filter(person_name=name).last()
        else :
            return redirect ('users:person_is_here')

        task_name = 'show documents'
        documents = []
        person_tasks = TaskPerson.objects.filter(person_name=name)
        for task in person_tasks:
            document = Document.objects.get(code=task.code)
            documents.append(document)
        return render(request,'documents/show_documents.html',{'emperson':emperson,'documents':documents,'task_name':task_name})



def done_task(request):
    document_code = request.session.get('document_code','0')
    document = Document.objects.get(code=document_code)
    document.done = True
    document.save()
    del request.session['document_code']
    return redirect('documents:show_documents')

costs = {'family register':1000,
               'birth register':1000,
                'marriage register':1000,
                'divorce register':1000,
                'death register':1000,
                'add information' : 1000,
                'add person':1000,
                'add parent':1000,
                'add marrid' : 1000,
                'add divorce':1000,
                'add widower':1000,
                'death record':1000
               }

def insert_task(request):
        name = user_is_logined(request=request)
        person = Person.objects.get(person_name=name)
        if not person.is_employee:
            last_document = Document.objects.order_by('code').last()
            if last_document:
                code = int(last_document.code) + 1
                code = str(code).zfill(8)
            name = user_is_logined(request=request)
            task_name = request.session.get('task_name','0')
            person_national_num = Person.objects.get(person_name=name).national_num
            second_national_num =request.session.get('second_national_num',None)
            viewed = False
            notes = '  '
            document = Document(name=task_name,code=code,person_national_num=person_national_num,second_national_num=second_national_num,viewed=viewed,notes=notes)
            document.save()
            user = User.objects.get(username=person.person_name)
            cost =costs[task_name]
            order = Order(user=user,code=code,cost=cost)
            order.save()
            del request.session['task_name']
            request.session['second_national_num']='ads'
            del request.session['second_national_num']
        return redirect('users:main')


def insert_task_code(request):
    last_document = Document.objects.order_by('code').last()
    if last_document:
        code = int(last_document.code) + 1
        code = str(code).zfill(8)
    person = get_person(request)
    task_name = request.session.get('task_name','0')
    person_national_num = person.national_num
    second_national_num =request.session.get('second_national_num',None)
    viewed = False
    notes = '  '
    document = Document(
        name=task_name,
        code=code,
        person_national_num=person_national_num,
        second_national_num=second_national_num,
        viewed=viewed,
        notes=notes
        )
    document.save()
    user = User.objects.get(username=person.person_name)
    cost =costs[task_name]
    order = Order(user=user,code=code,cost=cost)
    order.save()
    del request.session['task_name']
    request.session['second_national_num']='ads'
    del request.session['second_national_num']
    return code

def insert_document(request):

        document_code = request.session.get('document_code','0')
        document = Document.objects.get(code=document_code)
        document_name = document.name
        choices = {
            'family register':'documents:family_register',
            'birth register':'documents:birth_register',
            'marriage register':'documents:show_marriage_register',
            'divorce register':'documents:show_marriage_register',
            'dead register':'documents:dead_register_show',
            'add information' : 'users:information_save',
            'add person':'users:person_save',
            'add parent':'users:parent_save',
            'add marrid' : 'users:add_marrid',
            'add divorce':'users:add_divorce',
            'add widower':'users:add_widower',
            'death record':'users:death_save'
            }
        path = choices [document_name]
        url = path
        return redirect(url)



