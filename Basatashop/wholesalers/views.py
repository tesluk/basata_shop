from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from Basatashop.Entities.models import DocumentFile, Company
from django.template.context import RequestContext
import os, mimetypes
from Basatashop.Entities.contex_generator import get_base_context

def wholesale(request):
    docs = DocumentFile.objects.all().order_by("-id")
    for doc in docs:
        doc.doc_file_name = doc.doc_file.__unicode__().split('/')[-1]
    c = RequestContext(request, {'user':request.user})
    mc = get_base_context(request)
    c.dicts += mc.dicts
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/news/')
    if request.user.is_staff or len(Company.objects.filter(user=request.user))!=0:
        return render_to_response('wholesalers/wholesale.html', {'docs': docs}, c)
    else:
        return HttpResponseRedirect('/add_company/')

def add_company(request):
    c = RequestContext(request, {'user' : request.user})
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return render_to_response('wholesalers/add_company.html', c)

def submit_company(request):
       
    com = Company(
                  user = request.user,
                  name = request.POST.get('name'), 
                  tel = request.POST.get('tel'),
                  city = request.POST.get('city'),
                  address = request.POST.get('address'),
                  post = request.POST.get('post'),
                  description = request.POST.get('description'))
    com.save()
    return HttpResponseRedirect('/wholesale/')

def file_download(request, _id):
    header = DocumentFile.objects.filter(id=_id)[0]
    mimetype = mimetypes.guess_type(os.path.basename(header.doc_file.name))[0]
    print mimetype
    f = open(header.doc_file.path, 'rb')
    return HttpResponse(f, mimetype=mimetype)

def file_delete(request, _id):
    file = DocumentFile.objects.filter(id=_id)[0].delete()
    return HttpResponseRedirect('/wholesale/')
    
def add_doc(request):
    c = RequestContext(request, {'user' : request.user})
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return render_to_response('wholesalers/add_doc.html', {}, c)

def submit_doc(request):
    n = DocumentFile(doc_type = "tmp", description = request.POST['text'], doc_file = request.FILES['doc'])
    n.save()
    tip = n.doc_file.__unicode__().split('/')[-1].split('.')[1]
    n.doc_type = tip;
    n.save()
    return HttpResponseRedirect('/wholesale/')

def edit_company(request):
    c = RequestContext(request, {'user' : request.user})
    mc = get_base_context(request)
    c.dicts += mc.dicts
    com = Company.objects.filter(user = request.user)[0]   
    return render_to_response('wholesalers/edit_company.html', {'n': com.name, 't': com.tel, 'c':com.city, 'a':com.address, 'p': com.post, 'd' : com.description})

def esubmit_company(request):
    c = RequestContext(request, {'user' : request.user})   
    p = Company.objects.filter(user = request.user)[0]
    p.name = request.POST.get('name') 
    p.tel = request.POST.get('tel')
    p.city = request.POST.get('city')
    p.address = request.POST.get('address')
    p.post = request.POST.get('post')
    p.description = request.POST.get('description')
    p.save()
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponseRedirect('/')