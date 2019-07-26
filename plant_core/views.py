from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from plant_core.models import (Enclosure,
                               Cooler,
                               VaporGenerator,
                               WaterTank,
                               Heater,
                               UvLight,
                               CO2Valve,
                               Filters,
                               SimpleFlaps)

from plant_core.serializers import (EnclosureSerializer,
                                    CoolerSerializer,
                                    VaporGeneratorSerializer,
                                    WaterTankSerializer,
                                    HeaterSerializer,
                                    UvLightSerializer,
                                    CO2ValveSerializer,
                                    FiltersSerializer,
                                    SimpleFlapsSerializer)


class EnclosureView(GenericAPIView):
    serializer_class = EnclosureSerializer

    @csrf_exempt
    def post(self, request):
        serializer = EnclosureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = EnclosureSerializer(Enclosure.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CoolerView(GenericAPIView):
    serializer_class = CoolerSerializer

    @csrf_exempt
    def post(self, request):
        serializer = CoolerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = CoolerSerializer(Cooler.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VaporGeneratorView(GenericAPIView):
    serializer_class = VaporGeneratorSerializer

    @csrf_exempt
    def post(self, request):
        serializer = VaporGeneratorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = VaporGeneratorSerializer(VaporGenerator.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WaterTankView(GenericAPIView):
    serializer_class = WaterTankSerializer

    @csrf_exempt
    def post(self, request):
        serializer = WaterTankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = WaterTankSerializer(WaterTank.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HeaterView(GenericAPIView):
    serializer_class = HeaterSerializer

    @csrf_exempt
    def post(self, request):
        serializer = HeaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = HeaterSerializer(Heater.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UvLightView(GenericAPIView):
    serializer_class = UvLightSerializer

    @csrf_exempt
    def post(self, request):
        serializer = UvLightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = UvLightSerializer(UvLight.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CO2ValveView(GenericAPIView):
    serializer_class = CO2ValveSerializer

    @csrf_exempt
    def post(self, request):
        serializer = CO2ValveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = CO2ValveSerializer(CO2Valve.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FiltersView(GenericAPIView):
    serializer_class = FiltersSerializer

    @csrf_exempt
    def post(self, request):
        serializer = FiltersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = FiltersView(Filters.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimpleFlapsView(GenericAPIView):
    serializer_class = SimpleFlapsSerializer

    @csrf_exempt
    def post(self, request):
        serializer = SimpleFlapsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = SimpleFlapsSerializer(SimpleFlaps.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
