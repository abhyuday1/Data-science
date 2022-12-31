from unicodedata import name
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.utils.timezone import datetime
from customer.models import OrderModel
# Create your views here.

class Dashboard(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self, request, *args, **kwargs):
        # get the current date time
        today=datetime.today()
        orders=OrderModel.objects.filter(created_on__year=today.year,created_on__month=today.month,created_on__day=today.day)

        #lopp through the orders and add the price values
        total_revenue=0

        for order in orders:
            total_revenue+=order.price
        # total numbe rof ordrers and total revenue

        context={
            'orders':orders,
            'total_revenue':total_revenue,
            'total_order':len(orders)
        }
        print(10)
        return render(request, 'restaurant/dashboard.html',context)

    def post(self,request,id,*args,**kwargs):
        order=OrderModel.objects.get(orderid=id)
        order.is_served=True
        order.save()

        context={
            'order':order
        }

        return render(request, 'restaurant/dashboard.html',context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()


