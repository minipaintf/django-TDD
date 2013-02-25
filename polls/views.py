# Create your views here.
from django.http import HttpResponse
from polls.models import Poll
from django.shortcuts import render
from polls.forms import PollVoteForm


def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)
    # content = ''
    # for poll in Poll.objects.all():
    #     content += poll.question
        
    # return HttpResponse(content)

def poll(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    form = PollVoteForm(poll=poll)
    return render(request, 'poll.html',{'poll': poll, 'form':form})
