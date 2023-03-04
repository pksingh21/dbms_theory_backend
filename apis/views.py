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
from .models import FunctionalDependency, SetOfAttributes, BuisnessLogic


class FunctionalDependencyViewSet(viewsets.ModelViewSet):
    queryset = FunctionalDependency.objects.all()
    serializer_class = FunctionalDependencySerializer


class SetOfAttributesViewSet(viewsets.ModelViewSet):
    queryset = SetOfAttributes.objects.all()
    serializer_class = SetOfAttributesSerializer

    lookup_field = "pk"

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            # Custom logic to retrieve additional data about the object
            extra_data = {
                "some_field": instance.some_field,
                "another_field": instance.another_field,
            }
            # Combine the serialized object data with the additional data
            serialized_data = self.serializer_class(instance).data
            serialized_data.update(extra_data)
            return Response(serialized_data)
        except:
            return Response({"detail": "Object notx found."}, status=404)

    def create(self, request):
        query = request.data["data"]["query"]
        attributes = request.data["data"]["attributes"]
        left = request.data["data"]["left"]
        right = request.data["data"]["right"]
        print(query)
        Attributes = SetOfAttributes.objects.create(attributes=attributes)
        FunctionalDependencyArray = list()
        functionalDependencyArrayNotSETData = list()
        id_array_functionalDependency = list()
        for i in range(len(left)):
            FunctionalDependencyi = FunctionalDependency.objects.create(
                left=left[i], right=right[i]
            )
            print(left[i], right[i], "FunctionalDependencyi")
            functionalDependencyArrayNotSETData.append(
                {"left": left[i], "right": right[i]}
            )
            FunctionalDependencyArray.append(FunctionalDependencyi)
            id_array_functionalDependency.append(FunctionalDependencyi.id)
        # print(str(Attributes),str(FunctionalDependencyArray))
        Attributes.FunctionalDependency.set(FunctionalDependencyArray)
        id_attributes = Attributes.id
        # Buisness Logic starts
        BuisnessLogicInstance = BuisnessLogic()
        candidate_keys = BuisnessLogicInstance.calculateCandidateKeys(
            attributes, functionalDependencyArrayNotSETData
        )
        prime_attributes = BuisnessLogicInstance.findPrimeAttributes(
            candidate_keys)
        non_prime_attributes = BuisnessLogicInstance.findNonPrimeAttributes(
            attributes=attributes, prime_attributes=prime_attributes
        )
        response_object = {}

        if query == "Find Minimal Cover/Find 3NF Other Method":
            # exec minimal cover functions
            print("Find Minimal Cover")
            minimal_cover = BuisnessLogicInstance.findMinimalCover(
                attributes=attributes, fds=functionalDependencyArrayNotSETData
            )
            response_object['minimal_cover'] = minimal_cover
        elif query == "Find Candidate Keys":
            print("alright candidate keys")
            response_object['candidate_keys'] = candidate_keys
        elif query == "Check Normal Form":
            print("check normal form")
            normal_form = BuisnessLogicInstance.whichNormalForm(
                prime_attributes=prime_attributes,
                non_prime_attributes=non_prime_attributes,
                candidate_keys=candidate_keys,
                fds=functionalDependencyArrayNotSETData,
            )
            response_object['normal_form'] = normal_form
        elif (
            query == "Normalize to 2NF"
            or query == "Normalize to 3NF"
            or query == "Normalize to BCNF"
        ):
            NFForm_1 = BuisnessLogicInstance.return1NFForm(
                attributes=attributes,
                fds=functionalDependencyArrayNotSETData,
                cadidate_keys=candidate_keys,
                prime_attributes=prime_attributes,
                non_prime_attributes=non_prime_attributes,
            )
            NFForm_2 = BuisnessLogicInstance.return2NFForm(
                relation_1NF=NFForm_1)
            NFForm_3 = BuisnessLogicInstance.return3NFForm(
                relation_2NF=NFForm_2)
            BCNF_Form = BuisnessLogicInstance.returnBCNF(relation_3NF=NFForm_3)
            LossLessJoinMatrix = BuisnessLogicInstance.LossLessJoinTester(
                relation_1NF=NFForm_1,
                relation_BCNF=BCNF_Form,
            )
            if query == "Normalize to 2NF":
                response_object['NFForm_2'] = NFForm_2
            if query == "Normalize to 3NF":
                response_object['NFForm_3'] = NFForm_3
            if query == "Normalize to BCNF":
                response_object['BCNF_Form'] = BCNF_Form
            response_object['LossLessJoinMatrix'] = LossLessJoinMatrix
            print(LossLessJoinMatrix, "lossless join matrix")
        return Response(
            {
                "info": "data was posted successfully",
                "data": {
                    "id_attributes": id_attributes,
                    "id_functional_dependency": id_array_functionalDependency,
                    "query": query,
                    "queryResult": response_object,
                },
            },
            status=status.HTTP_201_CREATED,
        )
