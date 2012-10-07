from django.template.context import RequestContext    
from Basatashop.Entities.models import Product_group, Product_type, Basket

def get_base_context(request):
    
    c = RequestContext(request, {})
    
    c.dicts.append({ 'user':request.user })
    
    if "basket" in request.session:
        basket = request.session['basket']
        if not basket:
            basket = Basket()
            basket.orders = []
        delete_zeros(basket)
        request.session['basket'] = basket
        c.dicts.append({'basket': basket})
    
    grs = Product_group.objects.all()
       
    links = list(grs)
    
    for l in links:
        tps = Product_type.objects.all().filter(group=l)
        l.sublinks = list(tps)
    
    c.dicts.append({'links':links})
    return c

def delete_zeros (basket):
    
    neworders = []
    
    for o in basket.orders:
        if int(o.numb) != 0:
            neworders.append(o)
    
    basket.orders = neworders
    basket.size = len(basket.orders)