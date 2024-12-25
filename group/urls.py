from django.urls import path
import group.views

urlpatterns = [
    path('group/', group.views.GroupList.as_view()),
    path('group/register/', group.views.GroupList.as_view()),
    path('group/<str:name>/', group.views.GroupDetail.as_view())
]
