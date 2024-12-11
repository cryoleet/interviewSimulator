from django.http import HttpResponse
from django.shortcuts import render
import json


def selectInterview(request):
  return render(request=request, template_name="select_interview.html")


def topics(request):
  if request.method == "POST":
    topicList = request.POST.get("topicList", [])
    return HttpResponse(topicList)  
  

def interview_questions(request):
  questions = [
      "What are your strengths?",
      "Where do you see yourself in 5 years?",
      "Describe a challenging project you've worked on.",
      "Why do you want this role?",
      "What makes you unique?"
  ]
  return render(request, 'questions_test.html', {'questions': json.dumps(questions)})