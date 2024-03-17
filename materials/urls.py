from django.urls import path
from rest_framework import routers

from materials.apps import MaterialsConfig
from materials.views.lesson import *
from materials.views.course import *
from users.views.subscription import SubscribeAPIView

app_name = MaterialsConfig.name


urlpatterns = [
    path('', LessonListView.as_view(), name='lesson_list'),
    path('<int:pk>/', LessonDetailView.as_view()),
    path('<int:pk>/update/', LessonUpdateView.as_view(), name='lesson_update'),
    path('create/', LessonCreateView.as_view(), name='lesson_create'),
    path('<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('subscription/', SubscribeAPIView.as_view(), name='subscription'),

]

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns += router.urls

