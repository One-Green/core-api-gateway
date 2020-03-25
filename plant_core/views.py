from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from plant_core.models import (
    Enclosure,
    Cooler,
    AirHumidifier,
    WaterPump,
    SprinklerTag,
    SprinklerValve,
    Heater,
    UvLight,
    CO2Valve,
    Filters,
    SimpleFlaps
)

from plant_core.serializers import (
    EnclosureSerializer,
    CoolerSerializer,
    AirHumidifierSerializer,
    WaterPumpSerializer,
    SprinklerValveSerializer,
    HeaterSerializer,
    UvLightSerializer,
    CO2ValveSerializer,
    FiltersSerializer,
    SimpleFlapsSerializer
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
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = EnclosureSerializer(Enclosure.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class CoolerView(GenericAPIView):
    serializer_class = CoolerSerializer

    @csrf_exempt
    def post(self, request):
        serializer = CoolerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "CoolerView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = CoolerSerializer(Cooler.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class AirHumidifierView(GenericAPIView):
    serializer_class = AirHumidifierSerializer

    @csrf_exempt
    def post(self, request):
        serializer = AirHumidifierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "VaporGeneratorView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = AirHumidifierSerializer(AirHumidifier.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class WaterPumpView(GenericAPIView):
    serializer_class = WaterPumpSerializer

    @csrf_exempt
    def post(self, request):
        serializer = WaterPumpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "WaterPumpView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = WaterPumpSerializer(WaterPump.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class SprinklerValveView(GenericAPIView):
    serializer_class = SprinklerValveSerializer

    @csrf_exempt
    def post(self, request):
        serializer = SprinklerValveSerializer(data=request.data)
        if serializer.is_valid():
            tag_created = False
            try:
                tag = SprinklerTag.objects.get(tag=request.data['tag'])
            except SprinklerTag.DoesNotExist:
                tag = SprinklerTag(tag=request.data['tag'])
                tag.save()
                tag_created = True
            finally:
                SprinklerValve(
                    tag=tag,
                    soil_hygrometry=request.data['soil_hygrometry']
                ).save()

            return Response(
                {
                    'type': "SprinklerValveView",
                    'tag': tag.tag,
                    'tag_created': tag_created,
                    'saved': True
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'type': "SprinklerValveView",
                    'error': True,
                    'message': 'Missing "tag", "soil_hygrometry" to process'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @csrf_exempt
    def get(self, request):
        serializer = SprinklerValveSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tag = SprinklerTag.objects.get(tag=request.data['tag'])
            except SprinklerTag.DoesNotExist:
                return Response(
                    {
                        'type': "SprinklerValveView",
                        'tag': request.data['tag'],
                        'error': True,
                        'saved': False,
                        'message': "Tag not found in database"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            r = model_to_dict(
                SprinklerValve.objects.filter(
                    tag=tag
                ).order_by('-created')[0]
            )
            return Response(r, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    'type': "SprinklerValveView",
                    'error': True,
                    'message': 'Missing "tag" to process'
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
        return Response(
            {
                'type': "HeaterView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = HeaterSerializer(Heater.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class UvLightView(GenericAPIView):
    serializer_class = UvLightSerializer

    @csrf_exempt
    def post(self, request):
        serializer = UvLightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "UvLightView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = UvLightSerializer(UvLight.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class CO2ValveView(GenericAPIView):
    serializer_class = CO2ValveSerializer

    @csrf_exempt
    def post(self, request):
        serializer = CO2ValveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "CO2ValveView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = CO2ValveSerializer(CO2Valve.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class FiltersView(GenericAPIView):
    serializer_class = FiltersSerializer

    @csrf_exempt
    def post(self, request):
        serializer = FiltersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "FiltersView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = FiltersView(Filters.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)


class SimpleFlapsView(GenericAPIView):
    serializer_class = SimpleFlapsSerializer

    @csrf_exempt
    def post(self, request):
        serializer = SimpleFlapsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(
            {
                'type': "SimpleFlapsView",
                'saved': True
            },
            status=status.HTTP_201_CREATED
        )

    @csrf_exempt
    def get(self, request):
        serializer = SimpleFlapsSerializer(SimpleFlaps.objects.all(), many=True)
        return Response(serializer.data[-1], status=status.HTTP_200_OK)
