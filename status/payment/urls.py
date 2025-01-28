from django.urls import path
from .views import view_orders, process_payment, confirm_payment, enter_payment_amount,get_payment,view_payments
app_name = 'payment'
urlpatterns = [
    path('orders/', view_orders, name='orders'),
    path('process_payment/', process_payment, name='process_payment'),
    path('confirm_payment/', confirm_payment, name='confirm_payment'),
    path('enter_payment_amount/', enter_payment_amount, name='enter_payment_amount'),
    path('get_payment/',get_payment,name='get_payment'),
    path('view_payments',view_payments,name='view_payments'),
    #path('',,name=''),
    #path('',,name=''),
    #path('',,name=''),
    #path('',,name=''),
    #path('',,name=''),
]
