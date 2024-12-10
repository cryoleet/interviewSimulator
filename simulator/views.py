from django.http import HttpResponse
from django.shortcuts import render


def selectInterview(request):
  return render(request=request, template_name="select_interview.html")


def topics(request):
  if request.method == "POST":
    topicList = request.POST.get("topicList", [])
    return HttpResponse(topicList)
  
  
def dashboard(request):
    return render(request, 'dashboard.html')