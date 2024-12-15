from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from simulator import views
from simulator.views import selectInterview, topics, interview_questions, feedback, throughJD, companySpec

urlpatterns = [
    path('admin/', admin.site.urls),
    path('select/', views.selectInterview, name='select_interview'),
    path('topics/', views.topics, name='topics'),
    path('interview/', views.interview_questions, name='interview_questions'),
    path('media/audio_uploads/', views.audio_upload, name='upload_audio'),
    path('feedback/', feedback),
    path('', views.selectInterview),
    path('jd/', throughJD),
    path('companyspec/', companySpec)
] 
