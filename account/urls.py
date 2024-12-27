from django.urls import path
import account.views

urlpatterns = [
    path('user/', account.views.UserList.as_view(), name='getUserList'),
    path('user/register/', account.views.UserList.as_view(), name='registerUser'),
    path('user/info/<str:user_id>/', account.views.UserDetail.as_view(), name='userDetail'),
    path('user/join/group/', account.views.UserJoinGruiop.as_view(), name='userJoinGroup'),
    path('user/activate/', account.views.UserActivate.as_view(), name='userActivateChange'),
    path('user/name/', account.views.UserName.as_view(), name='userNameCharge'),
    path('user/password/', account.views.UserPassword.as_view(), name='userPWCharge'),
    path('user/count/', account.views.UserCount.as_view(), name='userCountPlus'),
    path('token/', account.views.CustomTokenObtainPairView.as_view(), name='issueToken'),
]

