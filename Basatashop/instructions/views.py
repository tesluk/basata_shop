from Basatashop.Entities.models import Instruction
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from Basatashop.Entities.pic_resize import resize_picture
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.loader import get_template

def all_instructions(request):
    table = Instruction.objects.all() 
    if "user" in request.session: 
        return render_to_response("instructions/all_instruct.html", {'table' : table, 'user':request.session['user']}, context_instance=RequestContext(request))
    else:
        return render_to_response("instructions/all_instruct.html", {'table' : table}, context_instance=RequestContext(request))


def add_instruct(request):
        
    i = Instruction()
    i.name = request.POST['name']
    i.picture = request.FILES['img']
    i.text = request.POST['text']
    i.save()
    resize_picture(i)
    
    return HttpResponseRedirect('/instructions/')


def get_add_instruct (request):
    
    t = get_template('instructions/add_new.html')
    c = RequestContext(request, { }) 
    return HttpResponse(t.render(c))

def delete(request, _id):
    try:
        _id = int(_id)
    except ValueError:
        raise Http404()
    Instruction.objects.filter(id = _id).delete()
    return HttpResponseRedirect('/instructions/')

def edit(request, _id):
    try:
        _id = int(_id)
    except ValueError:
        raise Http404()
    inst = Instruction.objects.get(id = _id)
    if "user" in request.session: 
        return render_to_response("instructions/edit.html", {'inst' : inst, 'user':request.session['user']}, context_instance=RequestContext(request))
    else:
        return render_to_response("instructions/edit.html", {'inst' : inst}, context_instance=RequestContext(request))

def save_edited(request, _id):
    inst = Instruction.objects.get(id = _id)
    inst.name = request.POST['name']
    inst.picture = request.FILES['img']
    inst.text = request.POST['text'] 
    inst.save()
    resize_picture(inst)
    
    return HttpResponseRedirect('/instructions/')