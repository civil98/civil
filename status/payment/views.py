from django.shortcuts import render, redirect
from .models import Order, Payment, Balance
from documents.models import Document
from django.contrib.auth.models import User

def view_orders(request):
    error = ''
    orders = Order.objects.filter(user=request.user,status ='Pending')
    if not Balance.objects.filter(user=request.user).exists():
        Balance(user=request.user,balance=0).save()
    balance = Balance.objects.get(user=request.user)
    if request.method == "POST":
        selected_order_ids = request.POST.getlist('selected_orders')
        orders = Order.objects.filter(id__in=selected_order_ids)
        total_cost = sum(order.cost for order in orders)
        if total_cost > int(balance.balance) :
            error ='you do not have enough'
        else :
            balance.balance = int(balance.balance) - total_cost
            balance.save()
            for order in orders:
                order.status ='paid'
                order.save()
                document = Document.objects.get(code=order.code)
                document.paid = 'paid'
                document.save()
            orders = Order.objects.filter(user=request.user,status ='Pending')
    return render(request, 'payment/view_orders.html', {'orders': orders,'balance':balance,'error':error})

def process_payment(request):
    if request.method == "POST":
        selected_order_ids = request.POST.getlist('selected_orders')
        orders = Order.objects.filter(id__in=selected_order_ids)
        total_cost = sum(order.cost for order in orders)
        return render(request, 'payment/payment_page.html', {'total_cost': total_cost, 'orders': orders})

def get_payment(request):
    error = ''
    if request.method == "POST":
        transaction_id = request.POST.get('payment_reference')
        if Payment.objects.filter(transaction_id=transaction_id,status='proccessed').exists():
            payment = Payment.objects.get(transaction_id=transaction_id)
        else :
            payment = Payment(user=request.user,transaction_id=transaction_id)
        try :
            payment.save()
            error = 'the payment saved'
        except :
            error = 'try anathor transaction id'
    return render(request, 'payment/payment_page.html',{'error':error})


def view_payments(request):
    error = ''
    payments = Payment.objects.filter(user=request.user)
    if not payments.exists():
        error = 'you have no payments to show'
    return render(request, 'payment/view_payments.html', {'payments': payments,'error':error})



def confirm_payment(request):
    if request.method == "POST":
        total_cost = request.POST.get('total_cost')
        payment_reference = request.POST.get('payment_reference')
        selected_order_ids = request.POST.getlist('selected_orders')

        # Logic to deduct from user's balance and update orders
        # Here you might check the user's profile for balance

        Order.objects.filter(id__in=selected_order_ids).update(status='Paid')
        return redirect('view_orders')  # Redirect to success page

def enter_payment_amount(request):
    error = ''
    if request.method == "POST":
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')
        status = 'proccessed'
        try:
            if Payment.objects.filter(transaction_id=transaction_id,status=status).exists():
                error = 'Transaction ID is already exist'
            else:
                if Payment.objects.filter(transaction_id=transaction_id).exists():
                    payment = Payment.objects.get(transaction_id=transaction_id)
                    payment.amount = amount
                    payment.status = status
                    user_id = User.objects.get(username=payment.user).id
                    balance = Balance.objects.get(user=user_id)
                    balance.balance = int(balance.balance) + int(amount)
                    balance.save()
                else :
                    payment = Payment(amount=amount,transaction_id=transaction_id,status=status)
                payment.save()
                error = ' the payment saved'
        except Payment.DoesNotExist:
            return render(request, 'payment/enter_payment_amount.html', {'error': 'Transaction ID not found!'})
    return render(request, 'payment/enter_payment_amount.html', {'error': error})
