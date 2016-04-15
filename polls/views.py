import random,json
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.core import serializers
from django.db.models import Max
from .models import Question,Phpquestion,Userprof,ContactDetails,UserQuestions
from polls.forms import *


def test(request):
    return render(request, 'test.html')

def javaindex(request):
    if request.user.is_authenticated():
        javapool = list(Question.objects.all())
        random.shuffle(javapool)
        jlist = javapool[:10]
        request.session['jlist'] = [j.q_id for j in jlist]
        return render(request,'index.html',{'latest_question_list': jlist})
    else:
        return HttpResponseRedirect('/')

def javaresult(request):
    if request.user.is_authenticated():
        ch = []
        correct = 0
        idlist = request.session['jlist']
        jlist = []
        for i in idlist:
            jlist.append(Question.objects.get(pk=i))
        answers = []
        for j in jlist:
            answers.append(j.ans)

        for i in range(1,11):
            s = request.POST.get(str(i))
            if s:
                question, choice = s.split('-')
                ch.append(choice)
            else:
                ch.append(None)

        for i in range(0,10):
            if ch[i] == answers[i]:
                correct+=1

        lisst = zip(jlist,ch)

        up = Userprof.objects.create(username=request.user.username,subject='java',score=correct)

        return render(request,'result.html',{'qlist':lisst,'score':correct})
    else:
        return HttpResponseRedirect('/')

# def mixindex(request):
#     # if request.user.is_authenticated():
#     #     pool = list(Phpquestion.objects.all())
#     #     random.shuffle(pool)
#     #     mlist = pool[:5]
#     #     pool = list(Question.objects.all())
#     #     random.shuffle(pool)
#     #     nlist = pool[:5]
#     #     mlist.append(nlist)
#     #     return render(request,'index.html',{'latest_question_list':mlist})
#     if request.user.is_authenticated():
#         phppool = list(Mixquestion.objects.all())
#         random.shuffle(phppool)
#         phplist = phppool[:10]
#         request.session['phplist'] = [p.q_id for p in phplist]
#         return render(request,'index.html',{'latest_question_list': phplist})
#     else:
#         return HttpResponse("Please login before continuing.")



def phpindex(request):
    if request.user.is_authenticated():
        phppool = list(Phpquestion.objects.all())
        random.shuffle(phppool)
        phplist = phppool[:10]
        request.session['phplist'] = [p.q_id for p in phplist]
        return render(request,'index.html',{'latest_question_list': phplist})
    else:
        return HttpResponseRedirect('/')

def phpresult(request):
    if request.user.is_authenticated():
        ch = []
        correct = 0
        idlist = request.session['phplist']
        phplist = []
        for i in idlist:
            phplist.append(Phpquestion.objects.get(pk=i))
        answers = []
        for p in phplist:
            answers.append(p.ans)

        for i in range(1,11):
            s = request.POST.get(str(i))
            if s:
                question, choice = s.split('-')
                ch.append(choice)
            else:
                ch.append(None)
        
        for i in range(0,10):
            if ch[i] == answers[i]:
                correct+=1

        lisst = zip(phplist,ch)

        up = Userprof.objects.create(username=request.user.username,subject='php',score=correct)

        return render(request,'result.html',{'qlist':lisst,'score':correct})
    else:
        return HttpResponseRedirect('/')

def show_perfindex(request):
    if request.user.is_authenticated():
        userj = Userprof.objects.filter(username__exact=request.user.username,subject__exact='java')
        userp = Userprof.objects.filter(username__exact=request.user.username,subject__exact='php')
        return render(request,'performance.html',{'userj':userj,'userp':userp})
    else:
        return HttpResponseRedirect('/')

def show_javachart(request):
    if request.user.is_authenticated():
        userss = Userprof.objects.filter(username__exact=request.user.username,subject__exact='java')
        c=1
        array = [['TestNumber', 'Java'],[0,0]]
        tickcount = [0]
        for u in userss:
            temp=[]
            temp.append(int(c))
            temp.append(int(u.score))
            array.append(temp)
            tickcount.append(c)
            c+=1

        return render(request,'chart.html', {'array': json.dumps(array),'tickcount':json.dumps(tickcount)})
    else:
        return HttpResponseRedirect('/')

def show_phpchart(request):
    if request.user.is_authenticated():
        userss = Userprof.objects.filter(username__exact=request.user.username,subject__exact='php')
        c=1
        array = [['TestNumber', 'PHP'],[0,0]]
        tickcount = [0]
        for u in userss:
            temp=[]
            temp.append(int(c))
            temp.append(int(u.score))
            array.append(temp)
            tickcount.append(c)
            c+=1

        return render(request,'chart.html', {'array': json.dumps(array),'tickcount':json.dumps(tickcount)})
    else:
        return HttpResponseRedirect('/')

def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            FormObj = ContactDetails(username=contact_name,email=contact_email,content=form_content)
            FormObj.save()
            # Email the profile with the 
            # contact information
            template = get_template('polls/contact_template.txt')
            context = {'contact_name': contact_name,'contact_email': contact_email,'form_content': form_content,}
            content = template.render({'context':context})
            email = EmailMessage(
                "New contact form submission",
                content,
                "Quizzy" +'',
                ['quizzy2016@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return HttpResponseRedirect('contact')
    return render(request, 'polls/contact.html', {'form': form_class,})

def submitq(request):
    form_class = QuestionForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            FormObj = UserQuestions(username=contact_name,email=contact_email,question=form_content)
            FormObj.save()

            # Email the profile with the 
            # contact information
            template = get_template('polls/question1.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render({'context':context})
            email = EmailMessage(
                "User has Entered",
                content,
                "" +'',
                [''],
                headers = {'': contact_email }
            )
            email.send()
            return HttpResponseRedirect('/submitq')

    return render(request, 'polls/question.html', {'form': form_class,})


def javaleaderboard(request):
    p = Userprof.objects.values('username','subject').annotate(score=Max('score')).order_by('-score')
    jp = p.filter(subject__exact='java')
    return render(request, 'polls/leaderboard.html',{'p':jp})

def phpleaderboard(request):
    p = Userprof.objects.values('username','subject').annotate(score=Max('score')).order_by('-score')
    pp = p.filter(subject__exact='php')
    return render(request, 'polls/leaderboard.html',{'p':pp})