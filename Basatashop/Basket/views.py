from django.template.loader import get_template
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from Basatashop.Entities.contex_generator import get_base_context
from Basatashop.Entities.models import Basket, Product, Characteristic, Order
import datetime
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

def get_order (request):
    
    t =get_template('basket/order.html')
    if "user" in request.session:
        c = RequestContext(request, {'user':request.session['user']})
    else:
        c = RequestContext(request, { })
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))
    
def get_ready (request):
    
    basket = request.session['basket']
    basket.user = request.user
    basket.adding_time = datetime.datetime.now()
    basket.address = request.POST['address']
    basket.tel = request.POST['tel']
    basket.comment = request.POST['comment']
    basket.btype = u'R'
    
    basket.save()
    
    for o in basket.orders:
        o.basket = basket
        o.save()
    
    request.session['basket'] = None
    
    t =get_template('basket/ready.html')
    if "user" in request.session:
        c = RequestContext(request, {'order_id':basket.id, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'order_id':basket.id})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def update_basket(request):
    
    basket = request.session['basket']
    
    for o in basket.orders:
        num = request.POST['char' + str(o.characteristic.id)]
        o.numb = num
    
    basket.summ = get_basket_summ(basket)
    basket.size = len(basket.orders)
    request.session['basket'] = basket
    
    return HttpResponseRedirect('/basket')

def delete_char (request, ch_id):
    
    basket = request.session['basket']

    neworders =[]

    for o in basket.orders:
        if str(o.characteristic.id) != str(ch_id):
            neworders.append(o)

    basket.orders = neworders
            
    basket.summ = get_basket_summ(basket)
    basket.size = len(basket.orders)
    request.session['basket'] = basket
    
    return HttpResponseRedirect('/basket/')

def get_basket(request):
    
    t = get_template('basket/basket.html')
    if "user" in request.session:
        c = RequestContext(request, {'user':request.session['user']})
    else:        
        c = RequestContext(request, { })

    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def add_product (request, pr_id):
    
    pr = Product.objects.all().get(id=pr_id)
    
    if "basket" in request.session:
        basket = request.session['basket']
    else:
        basket = Basket()
        basket.orders = []
        
    characteristics = Characteristic.objects.all().filter(product=pr)
    
    for char in characteristics:
        num = request.POST['num' + str(char.id)]
        if not num:
            num = 0
        if is_char_in_basket(basket, char):
            for o in basket.orders:
                if o.characteristic.id == char.id:
                    o.numb =int(o.numb) + int(num)
        else:
            order = Order()
            order.basket = basket
            order.characteristic = char
            order.numb = num
            if num != 0:
                basket.orders.append(order)
            
    basket.summ = get_basket_summ(basket)
    basket.size = len(basket.orders)
    request.session['basket'] = basket
    
    return HttpResponseRedirect('/basket/')
        
def is_char_in_basket(basket, char):
    for ord in basket.orders:
        if char == ord.characteristic:
            return True
    return False

def get_basket_summ (basket):
    summ = 0
    for o in basket.orders:
        summ += float(o.numb) * float(o.characteristic.prise)
    return summ

#BODIA

def order_state (request):
    c = {}
    c.update(csrf(request))
    user1 = request.session['user']; 
    print user1.is_staff, user1.login
    if (user1.is_staff == 1):
        try:
            baskets = Basket.objects.filter(btype='R')
        except baskets.DoesNotExist:
            return HttpResponse("Error")
    else:
        try:
            baskets = Basket.objects.filter(user=user1)
        except baskets.DoesNotExist:
            return HttpResponse("Error")
    if "user" in request.session:
        return render_to_response('basket/order_state.html', {"baskets":  baskets, 'user':request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('basket/order_state.html', {"baskets":  baskets},context_instance=RequestContext(request))

def finish_order (request):
    c = {}
    c.update(csrf(request))
    basket_id = request.POST['basket_id']
    
    try:
        basket = Basket.objects.get(id=basket_id)
        basket.btype = 'F'
        basket.save() 
    except Basket.DoesNotExist:
        return HttpResponse("Error")
    return order_state(request)