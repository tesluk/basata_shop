"""
Views which allow users to create and activate accounts.

"""
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from Basatashop.registration.signals import user_activated
from django.contrib.auth import login
from Basatashop.registration.backends import get_backend
from Basatashop.Entities.models import SUser
from django.http import HttpResponseRedirect
import sha

def register(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None):
    """
    Allow a new user to register an account.

    The actual registration of the account will be delegated to the
    backend specified by the ``backend`` keyword argument (see below);
    it will be used as follows:

    1. The backend's ``registration_allowed()`` method will be called,
       passing the ``HttpRequest``, to determine whether registration
       of an account is to be allowed; if not, a redirect is issued to
       the view corresponding to the named URL pattern
       ``registration_disallowed``. To override this, see the list of
       optional arguments for this view (below).

    2. The form to use for account registration will be obtained by
       calling the backend's ``get_form_class()`` method, passing the
       ``HttpRequest``. To override this, see the list of optional
       arguments for this view (below).

    3. If valid, the form's ``cleaned_data`` will be passed (as
       keyword arguments, and along with the ``HttpRequest``) to the
       backend's ``register()`` method, which should return the new
       ``User`` object.

    4. Upon successful registration, the backend's
       ``post_registration_redirect()`` method will be called, passing
       the ``HttpRequest`` and the new ``User``, to determine the URL
       to redirect the user to. To override this, see the list of
       optional arguments for this view (below).
    
    **Required arguments**
    
    None.
    
    **Optional arguments**

    ``backend``
        The dotted Python import path to the backend class to use.

    ``disallowed_url``
        URL to redirect to if registration is not permitted for the
        current ``HttpRequest``. Must be a value which can legally be
        passed to ``django.shortcuts.redirect``. If not supplied, this
        will be whatever URL corresponds to the named URL pattern
        ``registration_disallowed``.
    
    ``form_class``
        The form class to use for registration. If not supplied, this
        will be retrieved from the registration backend.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    ``success_url``
        URL to redirect to after successful registration. Must be a
        value which can legally be passed to
        ``django.shortcuts.redirect``. If not supplied, this will be
        retrieved from the registration backend.
    
    ``template_name``
        A custom template to use. If not supplied, this will default
        to ``registration/registration_form.html``.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = backend.register(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value    
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)


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
    
def register_edit(request):   
    userId = request.user.id
    if not userId is None:
        try:
            user = User.objects.get(id=userId)
            if request.method == 'POST':
                if request.POST['new_password'] != "":
                    if request.POST['new_password'] == request.POST['confirmed_new_password']:
                        user.set_password(request.POST['new_password'])
                    else:
                        return render_to_response('login.html', context_instance=RequestContext(request))
                user.username = request.POST['username']
                user.email = request.POST['email']
                user.first_name = request.POST['first_sec_name']
                
                if request.POST.__contains__('get_spam'):
                    user.last_name = 1
                else:
                    user.last_name = 0
                user.save()           
                return HttpResponseRedirect('/')
            else:                  
                if user.last_name == '0':
                    get_spam = False
                else:
                    get_spam = True             
                return render_to_response('registration_edit_form.html', 
                                      {'username': user.username,
                                       'email': user.email,
                                       'first_sec_name': user.first_name,
                                       'get_spam': get_spam}, context_instance=RequestContext(request))        
        except User.DoesNotExist:               
                    return render_to_response('login.html', context_instance=RequestContext(request))