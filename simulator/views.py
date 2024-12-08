from django.shortcuts import render


def selectInterview(request):
  return render(request=request, template_name="select_interview.html")