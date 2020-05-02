from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from plant_core.models import HeaterController
from plant_core.serializers import HeaterSerializer


class HeaterView(GenericAPIView):
    serializer_class = HeaterSerializer

    @csrf_exempt
    def post(self, request):
        serializer = HeaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                power = HeaterController.objects.all()[0].power
            except IndexError:
                power = 0

            return Response(
                {"type": "HeaterView", "acknowledged": True, "power": power},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {
                    "type": "HeaterView",
                    "error": True,
                    "message": "Missing mandatory key(s) to process",
                    "power": 0,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
