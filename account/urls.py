from django.urls import path
import account.views

urlpatterns = [
    path('account/', account.views.UserList.as_view()),
    path('account/register/', account.views.UserList.as_view()),
    path('account/<str:user_id>/', account.views.UserDetail.as_view()),
    path('token/', account.views.CustomTokenObtainPairView.as_view()),
]

