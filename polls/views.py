# Create your views here.
from django.http import HttpResponse,Http
from polls.models import Poll,Choice
from django.shortcuts import render
from polls.forms import PollVoteForm


def home(request):
    context = {'polls': Poll.objects.all()}
    return render(request, 'home.html', context)

def poll(request, poll_id):
    if request.method == 'POST':
        choice = Choice.objects.get(id=request.POST['vote'])
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('polls.views.poll', args=[poll_id,]))
    
    poll = Poll.objects.get(pk=poll_id)
    form = PollVoteForm(poll=poll)
    return render(request, 'poll.html',{'poll': poll, 'form':form})

