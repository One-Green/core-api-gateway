from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from plant_core.models import (Enclosure,
                               PeltierCell,
                               VaporGenerator,
                               WaterTank,
                               ElectricalHeater,
                               UvLight,
                               CO2Valve,
                               Filters)

from plant_core.serializers import (EnclosureSerializer,
                                    PeltierCellSerializer,
                                    VaporGeneratorSerializer,
                                    WaterTankSerializer,
                                    ElectricalHeaterSerializer,
                                    UvLightSerializer,
                                    CO2ValveSerializer,
                                    FiltersSerializer)


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


class PeltierCellView(GenericAPIView):
    serializer_class = PeltierCellSerializer

    @csrf_exempt
    def post(self, request):
        serializer = PeltierCellSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = PeltierCellSerializer(PeltierCell.objects.all(), many=True)
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


class ElectricalHeaterView(GenericAPIView):
    serializer_class = ElectricalHeaterSerializer

    @csrf_exempt
    def post(self, request):
        serializer = ElectricalHeaterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({'saved': True}, status=status.HTTP_201_CREATED)

    @csrf_exempt
    def get(self, request):
        serializer = ElectricalHeaterSerializer(ElectricalHeater.objects.all(), many=True)
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
