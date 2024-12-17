from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import os
import json
from .gemini_helper import topicListPrompt, askGemini, feedbackPrompt, questions_schema, feedback_schema, companySpecificPrompt, JdPrompt
from .whisper_helper import transcribeAudio
from docx import Document
import PyPDF2


def selectInterview(request):
  return render(request=request, template_name="select_interview.html")


def topics(request):
  if request.method == "POST":
    topicList = request.POST.get("topicList", [])
    number_of_questions = request.POST.get("number_of_questions", 5)
    prompt = topicListPrompt.format(number_of_questions, topicList)
    list_of_questions = askGemini(prompt, questions_schema)
    print("*" * 10)
    print(prompt)
    print("*" * 10)
    print("*" * 10)
    print(list_of_questions)
    print("*" * 10)
    request.session["questions"] = list_of_questions
    request.session["number_of_questions"] = len(list_of_questions)
    return redirect("/interview")
  

def throughJD(request):
    if request.method == "POST":
        jdFile = request.FILES.get("jd")
        number_of_questions = request.POST.get("number_of_questions", 5)
        file_content = ""
        if jdFile:
            file_name = jdFile.name
            file_extension = os.path.splitext(file_name)[1].lower()
            
            if file_extension == ".txt":
                with open(jdFile, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    
            elif file_extension == ".docx":
                
                doc = Document(file)
                text = [p.text for p in doc.paragraphs]
                file_content = "\n".join(text)
                

            elif file_extension == ".pdf":
                
                with open(jdFile, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = [page.extract_text() for page in reader.pages]
                    file_content = "\n".join(text)

            else:
                raise TypeError("Invalid file type")


        prompt = JdPrompt.format(number_of_questions, file_content)

        list_of_questions = askGemini(prompt, questions_schema)
        request.session["questions"] = list_of_questions
        request.session["number_of_questions"] = len(list_of_questions)
        return redirect("/interview")
    

def companySpec(request):
    if request.method == "POST":
        companyName = request.POST.get("companyName")
        companyRole = request.POST.get("companyRole")
        number_of_questions = request.POST.get("number_of_questions", 5)
        prompt = companySpecificPrompt.format(number_of_questions, companyName, companyRole)
        list_of_questions = askGemini(prompt, questions_schema)
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


def home(request):
    return render(request, 'home.html')
  