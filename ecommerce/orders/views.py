from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
import smtplib


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
        return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form})


def send_mail(id_num, email_addr, total_cost):
    MGS = r'Wyślij ' + str(total_cost) + ' na konto: XXXX-XXXX-XXXX-XXXX, o tytule: ORDNUM' + str(id_num)
    mailserver = smtplib.SMTP('smtp.gmail.com')

    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()

    username = r'login'
    password = r'password'

    mailserver.login(username, password)
    mailserver.sendmail(username, email_addr, MGS)
    mailserver.close()
