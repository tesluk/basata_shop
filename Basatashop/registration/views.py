"""
Views which allow users to create and activate accounts.

"""
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from Basatashop.Entities.models import SUser
from django.http import HttpResponseRedirect
import sha

def sregister(request):
    if request.method == 'POST':
        if request.POST['username'] != "" and request.POST['first_name'] != "" and request.POST['last_name'] != "" and request.POST['email'] != "" and request.POST['password'] != "":
            if request.POST['password'] == request.POST['confirmed_password']:
                try:
                    user = SUser.objects.all().get(login=request.POST['username'])
                    return render_to_response('registration/registration_form.html',{'error':"User with such username already exists"},context_instance=RequestContext(request))
                except SUser.DoesNotExist:
                    cur_user = SUser()
                    cur_user.login = request.POST['username']
                    cur_user.first_name = request.POST['first_name']
                    cur_user.last_name = request.POST['last_name']
                    date = request.POST['birthday']
                    
                    cur_user.birthday = request.POST['birthday']
                    cur_user.country = request.POST['country']
                    cur_user.city = request.POST['city']
                    cur_user.street = request.POST['street']
                    cur_user.email = request.POST['email']
                    cur_user.password = request.POST['password']
                    cur_user.is_staff = 1
                    if request.POST.__contains__('get_spam'):
                        cur_user.getSpam = 1
                    else:
                        cur_user.getSpam = 0
                    cur_user.save()                      
                    return render_to_response('registration/registration_complete.html', context_instance=RequestContext(request))
            else:
                return render_to_response('registration/registration_form.html',{'error':"Wrong confirmed password"},context_instance=RequestContext(request))
        else:
            return render_to_response('registration/registration_form.html',{'error':"Please, fill all the necessary fields"},context_instance=RequestContext(request))
    else:
        return render_to_response('registration/registration_form.html',{'error':""},context_instance=RequestContext(request))

def sregister_edit(request):    
    cur_user = request.session['user']    
    if request.method == 'POST':
        if request.POST['username'] != "" and request.POST['first_name'] != "" and request.POST['last_name'] != "" and request.POST['email'] != "" and request.POST['password'] != "":
            if request.POST['password'] == request.POST['confirmed_password']: 
                try:
                    userExist = SUser.objects.all().get(login=request.POST['username'])
                    if userExist.login == cur_user.login:                        
                        cur_user.login = request.POST['username']
                        cur_user.first_name = request.POST['first_name']
                        cur_user.last_name = request.POST['last_name']                
                        cur_user.country = request.POST['country']
                        cur_user.city = request.POST['city']
                        cur_user.street = request.POST['street']
                        cur_user.email = request.POST['email']
                        cur_user.password = request.POST['password']
                        if request.POST.__contains__('get_spam'):
                            cur_user.getSpam = 1
                        else:
                            cur_user.getSpam = 0
                        if request.POST['birthday'] is None:
                            cur_user.birthday = request.POST['birthday']                     
                        cur_user.save()    
                        request.session['user'] = cur_user
                        return render_to_response('registration_edit_form.html',{'user':cur_user, 'success':"All the cnanges are successfully accepted"},context_instance=RequestContext(request))
                    else:
                        return render_to_response('registration_edit_form.html',{'error':"User with such username already exists", 'user':cur_user},context_instance=RequestContext(request))
                except SUser.DoesNotExist:
                    cur_user.login = request.POST['username']
                    cur_user.first_name = request.POST['first_name']
                    cur_user.last_name = request.POST['last_name']                
                    cur_user.country = request.POST['country']
                    cur_user.city = request.POST['city']
                    cur_user.street = request.POST['street']
                    cur_user.email = request.POST['email']
                    cur_user.password = request.POST['password']
                    if request.POST.__contains__('get_spam'):
                        cur_user.getSpam = 1
                    else:
                        cur_user.getSpam = 0
                    if request.POST['birthday'] is None:
                        cur_user.birthday = request.POST['birthday']                     
                    cur_user.save()    
                    request.session['user'] = cur_user
                    return render_to_response('registration_edit_form.html',{'user':cur_user, 'success':"All the cnanges are successfully accepted"},context_instance=RequestContext(request))                
            else:
                return render_to_response('registration_edit_form.html',{'error':"Wrong confirmation password", 'user':cur_user},context_instance=RequestContext(request))
        else:
            return render_to_response('registration_edit_form.html',{'error':"Wrong data. Changes are not accepted", 'user':cur_user},context_instance=RequestContext(request))
    else:        
        return render_to_response('registration_edit_form.html',{'error':"", 'user':cur_user},context_instance=RequestContext(request))

def login(request):    
        if request.method == 'POST':        
            try:
                user = SUser.objects.all().get(login=request.POST['username'])                        
                if user.password == request.POST['password']: 
                    user.is_authenticated = 1                              
                    request.session['user'] = user       
                    return render_to_response('index.html',{'user':user},context_instance=RequestContext(request))
                else:
                    return render_to_response('registration/login.html',{'error':"Wrong password"},context_instance=RequestContext(request))
            except SUser.DoesNotExist:
                return render_to_response('registration/login.html',{'error':"Wrong username"},context_instance=RequestContext(request))
        else:
            return render_to_response('registration/login.html',{'error':""},context_instance=RequestContext(request))

def logout(request):
    request.session['user'] = 0
    return render_to_response('registration/logout.html',{'user':request.session['user']},context_instance=RequestContext(request))