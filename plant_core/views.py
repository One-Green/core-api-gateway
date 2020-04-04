from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from plant_core.models import (
    SprinklerSoilHumiditySensor,
    SprinklerTag,
    SprinklerValve,
)

from plant_core.serializers import (
    EnclosureSerializer,
    SprinklerSerializer
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
                power = False

            return Response(
                {
                    'type': "SprinklerValveView",
                    'tag': tag.tag,
                    'tag_created': tag_created,
                    'saved': True,
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
                    'power': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
