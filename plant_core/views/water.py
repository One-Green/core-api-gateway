from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from plant_core.models import WaterController
from plant_core.serializers import WaterSerializer


class WaterView(GenericAPIView):
    serializer_class = WaterSerializer

    @csrf_exempt
    def post(self, request):
        serializer = WaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                power = WaterController.objects.all()[0].power
            except IndexError:
                power = 0

            return Response(
                {"type": "WaterView", "acknowledged": True, "power": power},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {
                    "type": "WaterView",
                    "error": True,
                    "message": "Missing mandatory key(s) to process",
                    "power": 0,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
