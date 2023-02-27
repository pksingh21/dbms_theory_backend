from django.db import models
from django.contrib.postgres.fields import ArrayField
from rest_framework.views import APIView
from rest_framework.response import Response
from .dbms_ck import (
    find_candidate_keys,
    find_prime_attributes,
    normalize_to_2nf,
    normalize_to_3nf,
    normalize_to_bcnf,
    LJ_tester,
    is_in_2NF,
    is_in_3NF,
    is_in_BCNF,
)
from .timepass import minimal_cover


class FunctionalDependency(models.Model):
    left = ArrayField(models.CharField(max_length=1000), default=list, max_length=10000)
    right = ArrayField(
        models.CharField(max_length=1000), default=list, max_length=10000
    )

    def __str__(self):
        return "Functional Dependency was created successfully"


class BuisnessLogic:
    def __init__(self):
        print("BuisnessLogic Class was created successfully")

    def calculateCandidateKeys(self, Attributes, fds):
        candidate_keys = find_candidate_keys(Attributes, fds)
        return candidate_keys

    def findPrimeAttributes(self, candidate_keys):
        prime_attributes = find_prime_attributes(candidate_keys)
        return prime_attributes

    def findNonPrimeAttributes(self, attributes, prime_attributes):
        non_prime_Attributes = set(attributes) - prime_attributes
        return non_prime_Attributes

    def return1NFForm(
        self, attributes, fds, cadidate_keys, prime_attributes, non_prime_attributes
    ):
        return [
            {
                "attributes": attributes,
                "fds": fds,
                "candidate_keys": cadidate_keys,
                "prime_attributes": prime_attributes,
                "non_prime_attributes": non_prime_attributes,
            }
        ]

    def return2NFForm(self, relation_1NF):
        return normalize_to_2nf(relation_1nf=relation_1NF)

    def return3NFForm(self, relation_2NF):
        return normalize_to_3nf(relation_2nf=relation_2NF)

    def returnBCNF(self, relation_3NF):
        return normalize_to_bcnf(relation_3nf=relation_3NF)

    def LossLessJoinTester(self, relation_1NF, relation_BCNF):
        return LJ_tester(relation_1NF, relation_BCNF)

    def findMinimalCover(self, attributes, fds):
        return minimal_cover(attributes, fds)

    def whichNormalForm(self,prime_attributes, non_prime_attributes, candidate_keys, fds):
        return {
            "2NF": is_in_2NF(
                prime_attributes, non_prime_attributes, candidate_keys, fds
            ),
            "3NF": is_in_3NF(
                prime_attributes, non_prime_attributes, candidate_keys, fds
            ),
            "BCNF": is_in_BCNF(
                prime_attributes, non_prime_attributes, candidate_keys, fds
            ),
        }


class SetOfAttributes(models.Model):
    attributes = ArrayField(
        models.CharField(max_length=1000), default=list, max_length=100000
    )
    # type: ignore
    FunctionalDependency = models.ManyToManyField(FunctionalDependency)

    def __str__(self):
        return self.attributes
