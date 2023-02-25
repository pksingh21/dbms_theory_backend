# import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

# import local data
from .serializers import (
    FunctionalDependencySerializer,
    SetOfAttributesSerializer,
)
from .models import FunctionalDependency, SetOfAttributes  


class FunctionalDependencyViewSet(viewsets.ModelViewSet):
    queryset = FunctionalDependency.objects.all()
    serializer_class = FunctionalDependencySerializer


class SetOfAttributesViewSet(viewsets.ModelViewSet):
    queryset = SetOfAttributes.objects.all()
    serializer_class = SetOfAttributesSerializer
    def retrieve(self, request, pk=None):
        print("hi in list")
        print(request)
        return Response({"hi": "data was getted successfully"})

    def create(self, request):
        print("hi in post")
        print(request.data)
        return Response({"hi": "data was posted successfully", "data": request.data})
