from django.db import models
from django.contrib.postgres.fields import ArrayField
from rest_framework.views import APIView
from rest_framework.response import Response


class FunctionalDependency(models.Model):
    left = models.CharField(max_length=200)
    right = models.CharField(max_length=200)

    def __str__(self):
        return self.left + " -> " + self.right


class SetOfAttributes(models.Model):
    attributes = ArrayField(models.CharField(max_length=1), default=list, max_length=20)
    FunctionalDependency = models.ManyToManyField(FunctionalDependency)
    def __str__(self):
        return self.attributes
