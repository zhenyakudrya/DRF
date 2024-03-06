from django.urls import path

from users.apps import UsersConfig
from users.views.payment import PaymentList
from users.views.users import (
    UserListAPIView, UserDetailAPIView, UserCreateAPIView, UserUpdateAPIView, UserDestroyAPIView
)

app_name = UsersConfig.name


urlpatterns = [
    path('payment/', PaymentList.as_view()),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path("delete/<int:pk>/", UserDestroyAPIView.as_view(), name='user_delete'),
]