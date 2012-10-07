from django.template.loader import get_template
from django.template.context import Context, RequestContext
from Basatashop.Entities.models import Question, News
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datetime_safe import datetime
from Basatashop.Entities.contex_generator import get_base_context

def get_quest_list (request):
    
    questions = Question.objects.all()
    t = get_template('questions/quest_list.html')
    c = RequestContext(request, { 'questions':questions })
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))


def delete_question (request, q_id):
    
    Question.objects.all().filter(id=q_id).delete()
    return HttpResponseRedirect('/questions/')


def add_answer (request, q_id):
    
    ans = request.POST.get("ans")
    quest = Question.objects.all().get(id=q_id)
    quest.answer = ans
    quest.save() 
    return HttpResponseRedirect('/questions/')

def add_quest (request):
    
    quest = Question()
    quest.fio = request.POST.get("fio")
    quest.mail = request.POST.get("email")
    quest.text = request.POST.get("text")
    quest.adding_time = datetime.now()
    quest.save()
    return HttpResponseRedirect('/questions/')
    

def get_add_answer (request, q_id):
    
    question = Question.objects.all().get(id=q_id)
    t = get_template('questions/answer.html')
    c = RequestContext(request, { 'quest':question })
    
    mc = get_base_context(request)
    c.dicts += mc.dicts
    return HttpResponse(t.render(c))