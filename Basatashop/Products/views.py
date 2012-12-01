from django.template.loader import get_template
from Basatashop.Entities.models import Product_group, Product_type, Product, Characteristic, Price
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from Basatashop.Entities.pic_resize import resize_picture
from Basatashop.Entities.contex_generator import get_base_context
from django.shortcuts import render_to_response
from PIL import Image
import os
import time
from datetime import datetime, timedelta

def get_last_price(pr_id):
    prices = Price.objects.all().filter(product=pr_id)
    price = prices.order_by('date_init')[len(list(prices))-1]
    return price

def add_picture(obj, new_name, typ):
    for i in range(2):
        try:
            os.rename(str(obj.picture), new_name)
            obj.picture = new_name
            break
        except:
            os.remove(new_name+typ)
            os.remove(new_name+'_l'+typ)
            os.remove(new_name+'_b'+typ)
    
def get_all_groups (request):    
    groups = Product_group.objects.all()
    t = get_template('products/groups_list.html')
    if "user" in request.session:
        c = RequestContext(request, {'prod_groups':groups, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'prod_groups':groups})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def get_prod_group (request, gr_id):    
    gr = Product_group.objects.all().get(id=gr_id)
    types = Product_type.objects.all().filter(group=gr)
    t = get_template('products/types_list.html')
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'prod_types':types, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr, 'prod_types':types})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def get_prod_type (request, gr_id, tp_id):    
    gr = Product_group.objects.all().get(id=gr_id)
    tp = Product_type.objects.all().get(id=tp_id)
    products = Product.objects.all().filter(prod_type=tp)
    t = get_template('products/products_list.html')
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'type':tp, 'products':products, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr, 'type':tp, 'products':products})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def get_prod (request, gr_id, tp_id, pr_id):
    
    pr = Product.objects.all().get(id=pr_id)
    gr = Product_group.objects.all().get(id=gr_id)
    tp = Product_type.objects.all().get(id=tp_id)
    price = get_last_price(pr_id)
    characs = Characteristic.objects.all().filter(product=pr)
    t = get_template('products/product_info.html')
    
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'type':tp, 'product':pr, 'characs':characs, 'price':price, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr, 'type':tp, 'product':pr, 'characs':characs, 'price':price})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))


def get_add_prod (request, tp_id):
    tp = Product_type.objects.all().get(id=tp_id)
    gr = tp.group
    t = get_template('products/product_add.html')
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'type':tp, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr, 'type':tp})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def get_add_type (request, gr_id):
    
    gr = Product_group.objects.all().get(id=gr_id)
    t = get_template('products/type_add.html')
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def get_add_group (request):
    
    t = get_template('products/group_add.html')
    if "user" in request.session:
        c = RequestContext(request, {'user':request.session['user'] })
    else:
        c = RequestContext(request, { })
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def get_add_char (request, pr_id):    
    t = get_template('products/charac_add.html')
    pr = Product.objects.all().get(id=pr_id)
    price = get_last_price(pr_id).value
    charac = Characteristic.objects.all().filter(product=pr_id)
    if "user" in request.session:
        c = RequestContext(request, {'product':pr, 'characs':charac, 'price' : str(price),'user':request.session['user']})
    else:        
        c = RequestContext(request, {'product':pr, 'characs':charac, 'price' : str(price)})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))

def add_type (request, gr_id):
    
    gr = Product_group.objects.all().get(id=gr_id)
    tp = Product_type()
    tp.group = gr
    tp.name = request.POST['name']
    if 'img' in request.FILES:
        tp.picture = request.FILES['img']
        tp.save()
        typ = str(tp.picture).split('.') 
        new_name = 'Entities/static/products/img_'+str(gr.id)+'_'+str(tp.id); 
        t = '.'+typ[len(typ)-1] 
        add_picture(tp, new_name, t)        
    else: 
        tp.picture = 'Entities/static/products/standart.png';    
    tp.save() 
    resize_picture(tp)    
    return HttpResponseRedirect('/products/' + str(gr.id) + '/')

def add_group (request):
    
    gr = Product_group()
    gr.name = request.POST['name']
    if 'img' in request.FILES:
        gr.picture = request.FILES['img']
        gr.save()
        typ = str(gr.picture).split('.') 
        new_name = 'Entities/static/products/img_'+str(gr.id)
        t = '.'+typ[len(typ)-1] 
        add_picture(tp, new_name, t)      
    else: 
        gr.picture = 'Entities/static/products/standart.png';        
    gr.save()
    resize_picture(gr)  
    return HttpResponseRedirect('/products/')

def add_char (request, pr_id):    
    pr = Product.objects.all().get(id=pr_id)
    pr.name = request.POST['name']
    pr.producer = request.POST['producer']
    pr.quantity = request.POST['quantity']
    pr.sdescription = request.POST['sdescr'] 
    if 'picture' in request.FILES:
        pr.picture = request.FILES['picture']
        pr.save()
        typ = str(pr.picture).split('.') 
        pt = Product_type.objects.all().get(id=pr.prod_type.id)
        new_name = 'Entities/static/products/img_'+str(pt.group.id)+'_'+str(pt.id)+'_'+str(pr.id)    
        t = '.'+typ[len(typ)-1] 
        add_picture(pr, new_name,t)
    if 'userfile' in request.FILES:       
        pr.model= request.FILES['userfile']
        pr.save()
        new_name = 'Entities/static/products/models_'+str(tp.group.id) + '_' + str(tp.id)+'_'+str(pr.id)+'.dae'
        for i in range(2):
            try:
                os.rename(str(pr.model), new_name)
                pr.model = new_name
                break
            except:
                os.remove(new_name)  
    pr.save() 
    resize_picture(pr) 
    price = Price()
    price.value = request.POST['price']
    price.product = pr
    price.date_init = datetime.today().date()
    price.save()
    Characteristic.objects.filter(product = pr).delete()
    ch = Characteristic()
    chr_name = str(1) 
    i = 1
    while chr_name in request.POST:
        ch = Characteristic()
        ch.product = pr;
        ch.name = request.POST[chr_name]
        ch.description = request.POST[str(i+100)]
        ch.save()
        i=i+1
        chr_name = str(i)    
    return HttpResponseRedirect('/products/' + str(pr.prod_type.group.id) + '/' + str(pr.prod_type.id) + '/' + str(pr.id) + '/')
          
    
def add_prod (request, tp_id): 
    tp = Product_type.objects.all().get(id=tp_id)
    pr = Product()
    pr.prod_type = tp
    pr.name = request.POST['name']
    pr.producer = request.POST['producer']
    pr.quantity = request.POST['quantity']
    pr.sdescription = request.POST['sdescr']
    if 'picture' in request.FILES:
        pr.picture = request.FILES['picture']
        if 'userfile' in request.FILES:
            pr.model= request.FILES['userfile']
            pr.save()
            new_name = 'Entities/static/products/models_'+str(tp.group.id) + '_' + str(tp.id)+'_'+str(pr.id)+'.dae'
            for i in range(2):   
                try:                    
                    os.rename(str(pr.model), new_name)
                    pr.model = new_name
                    break;
                except:
                    os.remove(new_name) 
        else: 
            pr.model = 'Entities/static/products/banana.dae';  

        pr.save() 
        typ = str(pr.picture).split('.') 
        new_name = 'Entities/static/products/img_'+str(tp.group.id) + '_' + str(tp.id)+'_'+str(pr.id)
        t = '.'+typ[len(typ)-1] 
        add_picture(pr, new_name, t)
    else: 
        pr.picture = 'Entities/static/products/standart.png';  
  
    pr.save()
    price = Price()
    price.value = request.POST['price']
    price.product = pr
    price.date_init = datetime.today().date()
    price.save()       
    ch = Characteristic()
    chr_name = 'ch'+str(1)+'_name' 
    i = 1
    while chr_name in request.POST:
        ch = Characteristic()
        ch.product = pr;
        ch.name = request.POST[chr_name]
        ch.description = request.POST['ch'+str(i)+'_value']
        ch.save()
        i=i+1
        chr_name = 'ch'+str(i)+'_name' 
       
    resize_picture(pr)           
    return HttpResponseRedirect('/products/' + str(tp.group.id) + '/' + str(tp.id) + '/')  

def delete_prod_group (request, gr_id):    
    Product_group.objects.all().get(id=gr_id).delete()    
    return HttpResponseRedirect('/products/')

def delete_prod_type (request, gr_id, tp_id):
    
    gr = Product_type.objects.all().get(id=tp_id).group
    Product_type.objects.all().get(id=tp_id).delete()
    
    return HttpResponseRedirect('/products/' + str(gr.id) + '/')

def delete_prod (request, gr_id, tp_id, pr_id):
    #tp = Product.objects.all().get(id=pr_id).group
    Product.objects.all().get(id=pr_id).delete()    
    return HttpResponseRedirect('/products/' + gr_id + '/' + tp_id + '/')


def get_all_groups_xml (request):
    
    groups = Product_group.objects.all()
    for gr in groups:
        gr.count = len(Product_type.objects.all().filter(group=gr))
    t = get_template('xml/groups.xml')
    if "user" in request.session:
        c = RequestContext(request, {'groups':groups, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'groups':groups})    
    return HttpResponse(t.render(c))


def get_types_xml (request, gr_id):
    
    gr = Product_group.objects.all().get(id=gr_id)
    
    types = Product_type.objects.all().filter(group=gr)
    
    for tp in types:
        tp.count = len(Product.objects.all().filter(prod_type=tp))
    
    t = get_template('xml/types.xml')
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'types':types, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr, 'types':types})    
    return HttpResponse(t.render(c))


def get_products_xml (request, tp_id):
    
    tp = Product_type.objects.all().get(id=tp_id)
    
    gr = tp.group
    
    products = Product.objects.all().filter(prod_type=tp)
    
    # TODO add prices
    
    t = get_template('xml/products.xml')
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'type':tp, 'products':products , 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr, 'type':tp, 'products':products})    
    return HttpResponse(t.render(c))


def get_product_xml (request, pr_id):
    
    prod = Product.objects.all().filter(id=pr_id)
    
    chars = Characteristic.objects.all().filter(product = prod)
    
    # TODO add price
    
    t = get_template('xml/product.xml')
    if "user" in request.session:
        c = RequestContext(request, {'product':prod, 'chars':chars, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'product':prod, 'chars':chars})    
    return HttpResponse(t.render(c))

