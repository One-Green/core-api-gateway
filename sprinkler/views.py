from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrySerializer
from .serializers import ConfigSerializer
from core.utils import get_now
from core.pk_rom.sprinkler import Sprinklers


class RegistryView(GenericAPIView):
    serializer_class = RegistrySerializer

    @csrf_exempt
    def post(self, request):
        serializer = RegistrySerializer(data=request.data)
        if serializer.is_valid():
            tag = request.data['tag']
            print(
                f"[{get_now()}] [INFO] "
                f"New Sprinkler with {tag=} "
                f"wan't to register ..."
            )
            if Sprinklers().is_tag_in_registry(tag):
                r = {"acknowledge": False}
                print(
                    f"[{get_now()}] [WARNING] "
                    f"This tag {tag=} is already in registry"
                )
            else:
                r = {"acknowledge": True}
                Sprinklers().add_tag_in_registry(tag)
                print(
                    f"[{get_now()}] [OK] "
                    f"New Sprinkler with {tag=} "
                )
            return Response(r, status=status.HTTP_200_OK)


class ConfigView(GenericAPIView):
    serializer_class = ConfigSerializer

    @csrf_exempt
    def get(self, request, tag):
        return Response(
            Sprinklers().get_config(tag),
            status=status.HTTP_200_OK
        )

    @csrf_exempt
    def post(self, request, tag):
        serializer = ConfigSerializer(data=request.data)
        if serializer.is_valid():
            if Sprinklers().update_config(
                    tag=tag,
                    soil_moisture_min_level=request.data['soil_moisture_min_level'],
                    soil_moisture_max_level=request.data['soil_moisture_max_level']
            ):
                r = True
            else:
                r = False
            return Response(
                {
                    "acknowledged": r,
                    "config": {
                        "tag": tag,
                        "soil_moisture_min_level": request.data['soil_moisture_min_level'],
                        "soil_moisture_max_level": request.data['soil_moisture_max_level'],
                    }
                },
                status=status.HTTP_200_OK
            )
