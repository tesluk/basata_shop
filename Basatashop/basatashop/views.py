# Create your views here.
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template.context import RequestContext


# model

# Redirect to login page
def index (request):
    c = {}
    c.update(csrf(request))
    if "user" in request.session:    
        return render_to_response('index.html', {'user':request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', {},context_instance=RequestContext(request))
        

def about (request):    
    c = {}
    c.update(csrf(request))
    if "user" in request.session:
        return render_to_response('about.html', {'user':request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('about.html', {},context_instance=RequestContext(request))

def contacts (request):
    c = {}
    c.update(csrf(request))
    if "user" in request.session:
        return render_to_response('contacts.html', {'user':request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('contacts.html', {},context_instance=RequestContext(request))

def delivery (request):
    c = {}
    c.update(csrf(request))
    if "user" in request.session:
        return render_to_response('delivery_terms.html', {'user':request.session['user']},context_instance=RequestContext(request))
    else:
        return render_to_response('delivery_terms.html', {},context_instance=RequestContext(request))