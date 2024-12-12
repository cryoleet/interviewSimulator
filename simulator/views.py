from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from .gemini_prompts import topicListPrompt, askGemini


def selectInterview(request):
  return render(request=request, template_name="select_interview.html")


def topics(request):
  if request.method == "POST":
    topicList = request.POST.get("topicList", [])
    topicList = ",".join(topicList)
    prompt = topicListPrompt.format(topicList)
    list_of_questions = askGemini(prompt)
    request.session["questions"] = list_of_questions
    return redirect("/interview")
  

def interview_questions(request):
  questions = request.session.get("questions")
  return render(request, 'questions_test.html', {'questions': json.dumps(questions)})


def feedback(request):
  return render(request, "feedback.html")