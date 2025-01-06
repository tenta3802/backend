from django.urls import path
import file.views

urlpatterns = [
    path('file/upload/', file.views.UploadFile.as_view(), name='uploadFile'),
    path('file/get/', file.views.GetOriginFile.as_view(), name='getOriginFile'),
    path('dump-file/upload/', file.views.UploadDumpFile.as_view(), name='getOriginFile'),
    path('dump-file/get/', file.views.GetDumpFile.as_view(), name='getOriginFile')
]