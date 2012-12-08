# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template.context import RequestContext
from Basatashop.Entities.models import SUser

def create_admin():
     try:
        admin = SUser.objects.all().get(login='admin')
     except SUser.DoesNotExist: 
        admin = SUser()
        admin.login = 'admin'
        admin.first_name = 'admin'
        admin.last_name = 'admin'    
        admin.birthday = '2012-12-21'            
        admin.country = 'Adminland'
        admin.city = 'Admin-city'
        admin.street = 'Admin str, 10'
        admin.email = 'admin@normal.email'
        admin.password = '123'
        admin.getSpam = 0
        admin.is_staff = 1
        admin.save()
        
def create_courier():
    try:
        courier = SUser.objects.all().get(login='courier')
    except SUser.DoesNotExist: 
        courier = SUser()
        courier.login = 'courier'
        courier.first_name = 'courier'
        courier.last_name = 'courier'  
        courier.birthday = '2012-12-21'              
        courier.country = 'Courierland'
        courier.city = 'Courier-city'
        courier.street = 'Courier str, 10'
        courier.email = 'courier@normal.email'
        courier.password = '123'
        courier.getSpam = 0
        courier.is_staff = 1
        courier.save()

# model

# Redirect to login page
def index (request):
    c = {}
    c.update(csrf(request))
    #### creating admin and courier ####
    create_admin()
    create_courier()
    
    if "user" in request.session:
        return render_to_response('index.html', {'user': request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', {},context_instance=RequestContext(request))

def about (request):
    c = {}
    c.update(csrf(request))
    if "user" in request.session:
        return render_to_response('about.html', {'user': request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('about.html', {},context_instance=RequestContext(request))

def contacts (request):
    c = {}
    c.update(csrf(request))
    if "user" in request.session:
        return render_to_response('contacts.html', {'user': request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('contacts.html', {},context_instance=RequestContext(request))

def delivery (request):
    c = {}
    c.update(csrf(request))
    if "user" in request.session:
        return render_to_response('delivery_terms.html', {'user': request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('delivery_terms.html', {},context_instance=RequestContext(request))   