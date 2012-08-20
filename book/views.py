from django.shortcuts import render_to_response
import datetime

def timenow(request):
    now = datetime.datetime.now()
    return render_to_response('time.html',{'now':now})
