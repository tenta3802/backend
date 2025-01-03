from django.urls import path
import file.views

urlpatterns = [
    path('file/upload/', file.views.UploadFile.as_view(), name='uploadFile')
]