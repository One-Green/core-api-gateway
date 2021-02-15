from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from light.serializers import RegistrySerializer
from light.serializers import ConfigSerializer
from core.utils import get_now
from light.models import Light, Registry


class RegistryView(GenericAPIView):
    serializer_class = RegistrySerializer

    @csrf_exempt
    def get(self, request):
        """
        Return list of light tag available on registry
        :param request:
        :return:
        """
        r = Registry.objects.values_list('tag', flat=True)
        return Response(r, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        """
        Add new light tag on registry
        :param request:
        :return:
        """
        serializer = RegistrySerializer(data=request.data)
        if serializer.is_valid():
            tag = request.data['tag']
            print(f"[{get_now()}] [INFO] New Light with {tag=} want to register ...")
            if Light().is_tag_in_registry(tag):
                r = {"acknowledge": False}
                print(f"[{get_now()}] [WARNING] This tag {tag=} is already in registry")
            else:
                r = {"acknowledge": True}
                Light().add_tag_in_registry(tag)
                print(f"[{get_now()}] [OK] New Light with {tag=} ")
            return Response(r, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "acknowledged": False,
                    "message": "Input data invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @csrf_exempt
    def delete(self, request):
        try:
            Registry.objects.get(tag=request.data['tag']).delete()
            return Response(
                {"acknowledge": True},
                status=status.HTTP_200_OK
            )
        except Registry.DoesNotExist:
            return Response(
                {"acknowledge": False},
                status=status.HTTP_404_NOT_FOUND
            )


class ConfigView(GenericAPIView):
    serializer_class = ConfigSerializer

    @csrf_exempt
    def get(self, request, tag):
        """
        Get configuration of specific light tag
        :param request:
        :param tag:
        :return:
        """
        r = Light().get_config(tag)
        if r:
            return Response(
                r,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": f"Configuration for {tag=} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @csrf_exempt
    def post(self, request, tag):
        """
        Set configuration for a specific tag
        :param request:
        :param tag:
        :return:
        """
        serializer = ConfigSerializer(data=request.data)
        if serializer.is_valid():
            if Light().update_config(
                    tag=tag,
                    on_time_at=request.data['on_time_at'],
                    off_time_at=request.data['off_time_at']
            ):
                r = True
            else:
                r = False
            return Response(
                {
                    "acknowledged": r,
                    "config": {
                        "tag": tag,
                        "on_time_at": request.data['on_time_at'],
                        "off_time_at": request.data['off_time_at'],
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "acknowledged": False,
                    "message": "Input data invalid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
