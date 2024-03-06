from rest_framework import generics, filters
from users.models import Payment
from users.serializers.payment import PaymentSerializer


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['payment_date']
    search_fields = ['course__title', 'lesson__title', 'payment_method']