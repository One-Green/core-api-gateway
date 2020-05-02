from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from plant_core.serializers import EnclosureSerializer


class EnclosureView(GenericAPIView):
    serializer_class = EnclosureSerializer

    @csrf_exempt
    def post(self, request):
        serializer = EnclosureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {"type": "EnclosureView", "acknowledged": True},
            status=status.HTTP_201_CREATED,
        )
