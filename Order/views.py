from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from Accounts.models import CustomerProfile
from .models import Order

@login_required
def orders(request):
    customer=get_object_or_404(CustomerProfile,user=request.user)
    return render(request,'Order/orders.html',{'orders':customer.orders.all().order_by('-created_at')})

@login_required
def order_detail(request, pk):
    customer=get_object_or_404(CustomerProfile,user=request.user)
    order=get_object_or_404(Order,pk=pk,customer=customer)
    return render(request,'Order/order_detail.html',{'order':order})
