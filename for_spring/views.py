from rest_framework import viewsets
from .serializers import TestSerializer
from .models import Test

# Create your views here.
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer