from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from materials.models import Course
from materials.paginators import CoursePaginator
from materials.serializers.course import CourseSerializer
from materials.utils import get_url_for_payment
from users.models import Payment
from users.permissions import IsModerator, IsOwner
from users.serializers.payment import PaymentSerializer


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_moderator:
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.user = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]


class CoursePaymentAPIView(APIView):
    serializer_class = PaymentSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data["course"]

        course_item = get_object_or_404(Course, pk=course_id)

        if course_item:
            url_for_payment = get_url_for_payment(course_item)
            message = 'Right id of course'
            data = {
                "user": user,
                "payment_date": "2024-03-13",
                "course": course_item,
                "amount": course_item.price,
                "payment_method": "Transfer",
                "url_payment": url_for_payment,
                "status": "Process",
            }
            payment = Payment.objects.create(data)
            payment.save()
            return Response({"message": message, "url": url_for_payment})
        else:
            message = 'Wrong id of course'
            return Response({"message": message})