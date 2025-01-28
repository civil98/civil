from django.shortcuts import render,redirect
from .forms import Sign_up,Log_in,Reset_pass,Check_id,Login_employee,SignUpForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from users.models import Person
from users.views import main,user_is_logined,add_person_information
from documents.views import show_documents
from django.http import HttpResponse
from django.contrib import messages
from allauth.account.views import SignupView, LoginView, ConfirmEmailView,PasswordChangeView,PasswordResetDoneView,PasswordResetView
from django.utils import translation
from django.conf import settings


'''
def check_pass(request):

        task_name = 'reset password'
        error=' '
        if request.method == "POST":
            data = Reset_pass(request.POST)
            if data.is_valid():
                new_password = request.POST['new_password']
                confirm_password = request.POST['confirm_password']
                if new_password == confirm_password :
                    user = request.user
                    user.password  = new_password
                    user.save()
                    return redirect(main)
                else:
                    error = 'the passwords not match'
            else:
                error = data.errors
        return render(request,'registering/pass.html',{'form':Reset_pass,'error':error,'task_name':task_name})



def reset_pass(request):

        task_name = 'type id'
        error=' '
        if request.method == "POST":
            data = Check_id(request.POST)
            if data.is_valid():
                person = Person.objects.get(person_name=request.user.username)
                national_num = person.national_num
                current_national_num = request.POST['national_num']
                if national_num == current_national_num :
                    return redirect(check_pass)
                else:
                    error = 'wrong id'
            else:
                error = data.errors
        return render(request,'registering/pass.html',{'form':Check_id,'error':error,'task_name':task_name})



def log_in(request):

        error=' '
        task_name = 'login'
        if request.method == "POST":
            data = Log_in(request.POST)
            if data.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user =  authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    if Person.objects.filter(person_name=username).exists():
                        return redirect(main)
                    else :
                        return redirect(add_person_information)
            else:
                error = data.errors
        return render(request,'registering/login.html',{'user':Log_in,'error':error,'task_name':task_name})



def sign_up(request):

        error=' '
        task_name = 'signup'
        if request.method == "POST":
            data = Sign_up(request.POST)
            if data.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = User.objects.create_user(username=username, password=password)
                user.save()
                if user is not None:
                    login(request,user)
                    if Person.objects.filter(person_name=username).exists():
                        return redirect(main)
                    else :
                        return redirect(add_person_information)
            else:
                error = data.errors
        return render(request,'registering/login.html',{'user':Sign_up,'error':error,'task_name':task_name})



def sign_up(request):
    error = None
    task_name = 'signup'

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)  # تسجيل الدخول مباشرة بعد التسجيل

            # تحقق من وجود شخص مرتبط بالاسم
            if Person.objects.filter(person_name=username).exists():
                return redirect('main')  # استخدم اسم URL
            else:
                return redirect('add_person_information')  # استخدم اسم URL
        else:
            error = form.errors  # استخدام الأخطاء من النموذج

    else:
        form = SignUpForm()  # إنشاء نموذج فارغ

    return render(request, 'registering/login.html', {
        'form': form,
        'error': error,
        'task_name': task_name
    })
'''
class CustomSignupView(SignupView):
    template_name = 'registering/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomLoginView(LoginView):
    template_name = 'registering/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'registering/confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registering/password_changeV.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registering/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registering/password_reset.html'

    def get(self, request, *args, **kwargs):
        user_language = request.session.get('django_language', 'en')
        translation.activate(user_language)
        return super().get(request, *args, **kwargs)

def change_language(request, lang):
    prev_lang = translation.get_language()
    if lang in dict(settings.LANGUAGES):
        if lang != prev_lang :
            translation.activate(lang)
            request.session['django_language'] = lang
    referer = request.META.get('HTTP_REFERER','/')
    new_referer = referer.replace(f'/{prev_lang}/',f'/{lang}/')
    return redirect(new_referer)


def log_out(request):
    try :
        person = Person.objects.get(person_name=request.user.username)
        person.is_employee = False
        logout(request)
        del request.session['employee']
    except:
        pass
    return redirect('registering:account_login')

def login_employee(request):
    error = ''
    person = Person.objects.get(person_name=request.user.username)
    if request.method == 'POST':
        password = request.POST['password']
        if password == '12345':
            person.is_employee = True
            person.save()
            return redirect('documents:show_documents')
        else :
            error = 'wrong password, please assert 12345'
    else :
        if person.is_employee :
            person.is_employee = False
            person.save()
            return redirect('users:main')
    return render(request, 'registering/login_employee.html',{'error':error})
