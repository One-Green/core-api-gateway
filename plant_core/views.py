from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from plant_core.models import (
    SprinklerSoilHumiditySensor,
    SprinklerTag,
    SprinklerValve,
    Heater,
    CoolerSensor, Cooler

)

from plant_core.serializers import (
    EnclosureSerializer,
    SprinklerSerializer,
    HeaterSerializer,
    CoolerSerializer
)


class EnclosureView(GenericAPIView):
    serializer_class = EnclosureSerializer

    @csrf_exempt
    def post(self, request):
        serializer = EnclosureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "EnclosureView",
                'acknowledged': True
            },
            status=status.HTTP_201_CREATED
        )


class SprinklerView(GenericAPIView):
    serializer_class = SprinklerSerializer

    @csrf_exempt
    def post(self, request):
        serializer = SprinklerSerializer(data=request.data)
        if serializer.is_valid():
            tag_created = False
            try:
                tag = SprinklerTag.objects.get(tag=request.data['tag'])
            except SprinklerTag.DoesNotExist:
                tag = SprinklerTag(tag=request.data['tag'])
                tag.save()
                tag_created = True
            finally:
                SprinklerSoilHumiditySensor(
                    tag=tag,
                    soil_humidity=request.data['soil_humidity']
                ).save()
            try:
                power = SprinklerValve.objects.filter(tag=tag)[0].power
            except IndexError:
                power = 0

            return Response(
                {
                    'type': "SprinklerValveView",
                    'tag': tag.tag,
                    'tag_created': tag_created,
                    'acknowledged': True,
                    'power': power
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'type': "SprinklerValveView",
                    'error': True,
                    'message': 'Missing "tag", "soil_humidity" to process',
                    'acknowledged': False,
                    'power': 0
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class HeaterView(GenericAPIView):
    serializer_class = HeaterSerializer

    @csrf_exempt
    def post(self, request):
        serializer = HeaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                power = Heater.objects.all()[0].power
            except IndexError:
                power = 0

            return Response(
                {
                    'type': "HeaterView",
                    'acknowledged': True,
                    'power': power
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {
                    'type': "HeaterView",
                    'error': True,
                    'message': 'Missing mandatory key(s) to process',
                    'power': 0
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class CoolerView(GenericAPIView):
    serializer_class = CoolerSerializer

    @csrf_exempt
    def post(self, request):
        serializer = CoolerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                t_power = Cooler.objects.all()[0].power_temperature
            except IndexError:
                t_power = 0
            try:
                h_power = Cooler.objects.all()[0].power_humidity
            except IndexError:
                h_power = 0

            if 1 in [t_power, h_power]:
                power = 1
            else:
                power = 0

            return Response(
                {
                    'type': "CoolerView",
                    'acknowledged': True,
                    'power': power
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {
                    'type': "CoolerView",
                    'error': True,
                    'message': 'Missing mandatory key(s) to process',
                    'power': 0
                },
                status=status.HTTP_400_BAD_REQUEST
            )
