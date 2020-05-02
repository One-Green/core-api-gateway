from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from plant_core.models import CoolerController
from plant_core.serializers import CoolerSerializer


class CoolerView(GenericAPIView):
    serializer_class = CoolerSerializer

    @csrf_exempt
    def post(self, request):
        serializer = CoolerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                t_power = CoolerController.objects.all()[0].power_temperature
            except IndexError:
                t_power = 0
            try:
                h_power = CoolerController.objects.all()[0].power_humidity
            except IndexError:
                h_power = 0

            if 1 in [t_power, h_power]:
                power = 1
            else:
                power = 0

            return Response(
                {"type": "CoolerView", "acknowledged": True, "power": power},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {
                    "type": "CoolerView",
                    "error": True,
                    "message": "Missing mandatory key(s) to process",
                    "power": 0,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
