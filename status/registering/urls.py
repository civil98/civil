from django.urls import path
from .views import log_out,login_employee,CustomSignupView,CustomConfirmEmailView,CustomLoginView,change_language,CustomPasswordChangeView,CustomPasswordResetDoneView,CustomPasswordResetView

app_name = 'registering'
urlpatterns = [
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='account_changepassword'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='account_resetdone'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='account_reset'),
    path('email/verify/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('log_out', log_out,name='log_out'),
    path('login_employee', login_employee,name='login_employee'),
    path('change-language/<str:lang>/', change_language, name='change_language'),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),
    #path('', ,name=''),

]
'''path('sign_up',sign_up ,name='sign_up'),
path('log_in',log_in ,name='log_in'),'''
