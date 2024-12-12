from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import os
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

@csrf_exempt
def audio_upload(request):
    if request.method == "POST" and request.FILES:
        files = request.FILES
        saved_files = []

        for key, audio_file in files.items():
            file_path = os.path.join('media', 'audio_uploads', audio_file.name)
            saved_path = default_storage.save(file_path, ContentFile(audio_file.read()))
            saved_files.append(saved_path)

        return JsonResponse({
            'message': 'Audio files uploaded successfully!',
            'files': saved_files,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

