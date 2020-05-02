from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from plant_core.models import (
    SprinklerSensor,
    SprinklerTag,
    SprinklerController
)
from plant_core.serializers import SprinklerSerializer


class SprinklerView(GenericAPIView):
    serializer_class = SprinklerSerializer

    @csrf_exempt
    def post(self, request):
        serializer = SprinklerSerializer(data=request.data)
        if serializer.is_valid():
            tag_created = False
            try:
                tag = SprinklerTag.objects.get(tag=request.data["tag"])
            except SprinklerTag.DoesNotExist:
                tag = SprinklerTag(tag=request.data["tag"])
                tag.save()
                tag_created = True
            finally:
                SprinklerSensor(
                    tag=tag, soil_humidity=request.data["soil_humidity"]
                ).save()
            try:
                power = SprinklerController.objects.filter(tag=tag)[0].power
            except IndexError:
                power = 0

            return Response(
                {
                    "type": "SprinklerValveView",
                    "tag": tag.tag,
                    "tag_created": tag_created,
                    "acknowledged": True,
                    "power": power,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "type": "SprinklerValveView",
                    "error": True,
                    "message": 'Missing "tag", "soil_humidity" to process',
                    "acknowledged": False,
                    "power": 0,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
