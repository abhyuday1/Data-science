from tkinter import Menubutton
from unicodedata import category
from django.shortcuts import render,redirect
from django.views import View
from .models import MenuItem,OrderModel,Category
# Create your views here.

class Index(View):
    def get(self, request,*args, **kwargs):
        return render(request,'customer/index.html')

class About(View):
    def get(self, request,*args, **kwargs):
        return render(request,'customer/about.html')

class Order(View):
    def get(self, request,*args, **kwargs):
        drinks=MenuItem.objects.filter(category__name__contains='Drink')
        breakfast=MenuItem.objects.filter(category__name__contains='Breakfast')
        dessert=MenuItem.objects.filter(category__name__contains='Dessert')
        # get every item from each category

        #pass into context
        context={
            'drink':drinks,
            'breakfast':breakfast,
            'dessert':dessert
        }
        # render the template
        return render(request,'customer/order.html',context)

    def post(self, request,*args, **kwargs):
        order_item={
            'items':[]
        }

        items=request.POST.getlist('items[]')

        for item in items:
            menu_item=MenuItem.objects.get(pk__contains=int(item))
            item_data= {
                'id':menu_item.pk,
                'name':menu_item.name,
                'price':menu_item.price
            }

            order_item['items'].append(item_data)

            price=0
            item_ids=[]

            for item in order_item['items']:
                price+=item['price']
                item_ids.append(item['id'])

            order=OrderModel.objects.create(price=price)
            order.items.add(*item_ids)

            context={
                'items':order_item['items'],
                'price':price
            }
            return redirect('order-confirmation',pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args,**kwargs):
        order=OrderModel.objects.get(pk=pk)

        context= {
            'pk':order.pk,
            'items':order.items,
            'pricr':order.price
        }
        return render(request,'customer/order_confirmation.html',context)

class OrderPayConfirmation(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/order_pay_confirmation.html')
