# import serializer from rest_framework
from rest_framework import serializers

# import model from models.py
from .models import  FunctionalDependency, SetOfAttributes 




class FunctionalDependencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FunctionalDependency
        fields = ("left", "right")


class SetOfAttributesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SetOfAttributes
        fields = ["attributes"]
