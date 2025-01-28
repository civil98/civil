from django.urls import path
from .views import person_in,main,parent_save,parent_in,index,user_is_logined,person_show,partner_in,assert_information,get_choice,death_record,person_save,add_person_information,add_marrid,add_divorce,add_widower,death_save,event_in,died_person_record,information_save,person_is_here,about

app_name = 'users'
urlpatterns = [

    path('person_in', person_in,name='person_in'),
    path('parent_save', parent_save,name='parent_save'),
    path('main', main,name='main'),
    path('parent_in', parent_in,name='parent_in'),
    path('index', index,name='index'),
    path('user_is_logined', user_is_logined,name='user_is_logined'),
    path('person_show',person_show ,name='person_show'),
    path('partner_in', partner_in,name='partner_in'),
    path('add_person_information',add_person_information ,name='add_person_information'),
    path('assert_information',assert_information ,name='assert_information'),
    path('get_choice',get_choice ,name='get_choice'),
    path('death_record',death_record ,name='death_record'),
    path('person_save', person_save,name='person_save'),
    path('add_marrid', add_marrid,name='add_marrid'),
    path('add_divorce', add_divorce,name='add_divorce'),
    path('add_widower', add_widower,name='add_widower'),
    path('death_save',death_save ,name='death_save'),
    path('event_in', event_in,name='event_in'),
    path('died_person_record',died_person_record ,name='died_person_record'),
    path('information_save',information_save ,name='information_save'),
    path('person_is_here', person_is_here,name='person_is_here'),
    path('about',about ,name='about'),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),

]
