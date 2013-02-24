# Create your views here.
from django.http import HttpResponse
from polls.models import Poll
from django.shortcuts import render

def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)
    content = ''
    for poll in Poll.objects.all():
        content += poll.question
        
    return HttpResponse(content)

