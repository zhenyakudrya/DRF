from django.urls import path
from rest_framework import routers

from materials.apps import MaterialsConfig
from materials.views.lesson import *
from materials.views.course import *

app_name = MaterialsConfig.name


urlpatterns = [
    path('', LessonListView.as_view()),
    path('<int:pk>/', LessonDetailView.as_view()),
    path('<int:pk>/update/', LessonUpdateView.as_view()),
    path('create/', LessonCreateView.as_view()),
    path('<int:pk>/delete/', LessonDeleteView.as_view()),

]

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns += router.urls

