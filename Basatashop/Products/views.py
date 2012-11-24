from django.template.loader import get_template
from Basatashop.Entities.models import Product_group, Product_type, Product, Characteristic
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from Basatashop.Entities.pic_resize import resize_picture
from Basatashop.Entities.contex_generator import get_base_context
from django.shortcuts import render_to_response
from Basatashop.Entities.models import SUser
from PIL import Image

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
    
    characs = Characteristic.objects.all().filter(product=pr)
    pr.characters = characs
    
    t = get_template('products/product_info.html')
    if "user" in request.session:
        c = RequestContext(request, {'group':gr, 'type':tp, 'product':pr, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'group':gr, 'type':tp, 'product':pr})
    
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
    if "user" in request.session:
        c = RequestContext(request, {'product':pr, 'user':request.session['user']})
    else:        
        c = RequestContext(request, {'product':pr})
    
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
    else: 
        gr.picture = 'Entities/static/products/standart.png';  
    gr.save()
    resize_picture(gr)    

    return HttpResponseRedirect('/products/')

def add_char (request, pr_id):
    
    pr = Product.objects.all().get(id=pr_id)
    ch = Characteristic()
    ch.size = request.POST['size']
    ch.charac_type = request.POST['char_type'] 
    ch.prise = request.POST['price']
    ch.product = pr
    ch.name = pr.name
    ch.save()    

    return HttpResponseRedirect('/products/' + str(pr.prod_type.group.id) + '/' + str(pr.prod_type.id) + '/' + str(pr.id) + '/')

def add_prod (request, tp_id):   
    tp = Product_type.objects.all().get(id=tp_id)
    pr = Product()
    pr.prod_type = tp
    pr.name = request.POST['name']
    pr.price = request.POST['price']
    pr.quantity = request.POST['quantity']
    pr.sdescription = request.POST['sdescr']
    pr.description = request.POST['descr']
    if 'picture' in request.FILES:
        pr.picture = request.FILES['picture']
    else: 
        pr.picture = 'Entities/static/products/standart.png';    
    if 'userfile' in request.FILES:
        pr.model3D = request.FILES['userfile']
    else: 
        pr.model3D = 'Entities/static/products/banana.dae';     
    pr.save()       
    ch = Characteristic()
    ch.product = pr;
    ch.name = request.POST['ch1_name']
    ch.charac_type = request.POST['ch1_value']
    ch.save()
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
    
    tp = Product.objects.all().get(id=pr_id).group
    Product.objects.all().get(id=pr_id).delete()
    
    return HttpResponseRedirect('/products/' + str(tp.group.id) + '/' + str(tp.id) + '/')


def get_all_groups_xml (request):
    
    groups = Product_group.objects.all()
    for gr in groups:
        gr.count = len(Product_type.objects.all().filter(group = gr))
    t = get_template('xml/groups.xml')
    if "user" in request.session:
        c = RequestContext(request, {'groups':groups, 'user':request.session['user']})
    else:
        c = RequestContext(request, {'groups':groups})    
    return HttpResponse(t.render(c))
