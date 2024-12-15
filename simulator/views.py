from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import os
import json
from .gemini_helper import topicListPrompt, askGemini, feedbackPrompt, questions_schema, feedback_schema
from .whisper_helper import transcribeAudio


def selectInterview(request):
  return render(request=request, template_name="select_interview.html")


def topics(request):
  if request.method == "POST":
    topicList = request.POST.get("topicList", [])
    topicList = ",".join(topicList)
    prompt = topicListPrompt.format(topicList)
    list_of_questions = askGemini(prompt, questions_schema)
    print("********************")
    print(list_of_questions)
    request.session["questions"] = list_of_questions
    request.session["number_of_questions"] = len(list_of_questions)
    return redirect("/interview")
  

def interview_questions(request):
  questions = request.session.get("questions")
  return render(request, 'questions_test.html', {'questions': json.dumps(questions)})

@csrf_exempt
def audio_upload(request):
    if request.method == "POST" and request.FILES:
        files = request.FILES
        saved_files = []

        for key, audio_file in files.items():
            file_path = os.path.join('media', 'audio_uploads', audio_file.name)

            if default_storage.exists(file_path):
                    default_storage.delete(file_path)

            saved_path = default_storage.save(file_path, ContentFile(audio_file.read()))
            saved_files.append(saved_path)
            print(saved_files)

        return JsonResponse({
            'message': 'Audio files uploaded successfully!',
            'files': saved_files,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


def feedback(request):
    
    answers = {}

    number_of_questions = request.session.get("number_of_questions")
    questions = request.session.get("questions")

    for i in range(number_of_questions):
        file_path = os.path.join('.', 'media', 'media', 'audio_uploads', f"question_{i + 1}.wav")

        transcribedText = transcribeAudio(filepath=file_path)

        answers[questions[i]] = transcribedText

    
    prompt = feedbackPrompt.format(answers)
    response = askGemini(prompt, feedback_schema)


    return render(request, "feedback.html", {"feedback" : response})

  