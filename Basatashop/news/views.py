from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from Basatashop.Entities.models import News
from django.template.context import Context, RequestContext
from Basatashop.Entities.pic_resize import resize_picture
from Basatashop.Entities.contex_generator import get_base_context

import smtplib
from smtplib import SMTPException
from Basatashop.Entities.models import SUser

def show_news(request):
    news = News.objects.order_by("-id")
    if "user" in request.session:
        c = RequestContext(request, {'user':request.session['user']})
    else:
        c = RequestContext(request, {})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return render_to_response('news/show_news.html', {'news': news}, c)

def add_news(request):
    if "user" in request.session:    
        c = RequestContext(request, {'user':request.session['user']})
    else:
        c = RequestContext(request, {})
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return render_to_response('news/add_news.html', {}, c)

def submit_news(request):
    tit =  request.POST['title']
    test = request.POST['text']
    img = request.FILES['img'] 
    n = News(title = tit, text = test, picture = img)
    n.save()
    
#    try:
#        smtp_server = 'smtp.gmail.com'
#        smtpObj = smtplib.SMTP(smtp_server, 587)
#        smtpObj.starttls()
#        login = 'basata.no.reply'
#        password = 'basata4ever'
#        smtpObj.login(login, password)
#        sender = 'basata.no.reply@gmail.com'
#        message = test
#        receivers = User.objects.filter(last_name='1')
#        
#        #receivers
#        for r in receivers:
#            smtpObj.sendmail(sender, r.email, message)
#            print 1
#              
#    except SMTPException:
#            print "Error: unable to send email"
    resize_picture ( n )
#    c = RequestContext({'user':request.user})
    return HttpResponseRedirect('/news/')
