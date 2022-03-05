from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from sprinkler.serializers import RegistrySerializer
from sprinkler.serializers import ConfigSerializer
from sprinkler.serializers import ForceControllerSerializer
from core.utils import get_now
from sprinkler.models import Sprinklers, Registry


class RegistryView(GenericAPIView):
    serializer_class = RegistrySerializer

    @csrf_exempt
    def get(self, request):
        """
        Return list of sprinkler tag available on registry
        :param request:
        :return:
        """
        r = Registry.objects.values_list("tag", flat=True)
        return Response(r, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        """
        Add new sprinkler tag on registry
        :param request:
        :return:
        """
        serializer = RegistrySerializer(data=request.data)
        if serializer.is_valid():
            tag = request.data["tag"]
            print(
                f"[{get_now()}] [INFO] "
                f"New Sprinkler with {tag=} "
                f"want to register ..."
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
                print(f"[{get_now()}] [OK] " f"New Sprinkler with {tag=} ")
            return Response(r, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request):
        try:
            Registry.objects.get(tag=request.data["tag"]).delete()
            return Response({"acknowledge": True}, status=status.HTTP_200_OK)
        except Registry.DoesNotExist:
            return Response({"acknowledge": False}, status=status.HTTP_404_NOT_FOUND)


class ConfigView(GenericAPIView):
    serializer_class = ConfigSerializer

    @csrf_exempt
    def get(self, request, tag):
        """
        Get configuration of specific sprinkler tag
        :param request:
        :param tag:
        :return:
        """
        return Response(Sprinklers().get_config(tag), status=status.HTTP_200_OK)

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
            if Sprinklers().update_config(
                tag=tag,
                soil_moisture_min_level=request.data["soil_moisture_min_level"],
                soil_moisture_max_level=request.data["soil_moisture_max_level"],
            ):
                r = True
            else:
                r = False
            return Response(
                {
                    "acknowledged": r,
                    "config": {
                        "tag": tag,
                        "soil_moisture_min_level": request.data[
                            "soil_moisture_min_level"
                        ],
                        "soil_moisture_max_level": request.data[
                            "soil_moisture_max_level"
                        ],
                    },
                },
                status=status.HTTP_200_OK,
            )


class ForceControllerView(GenericAPIView):
    """
    For debug only, force actuator status
    """

    serializer_class = ForceControllerSerializer

    @csrf_exempt
    def get(self, request, tag):
        """
        Get controller force status
        :param tag:
        :param request:
        :return:
        """
        return Response(
            Sprinklers().get_controller_force(tag), status=status.HTTP_200_OK
        )

    @csrf_exempt
    def post(self, request, tag):
        """
        Force pump off/on
        :param tag:
        :param request:
        :return:
        """
        serializer = ForceControllerSerializer(data=request.data)
        if serializer.is_valid():
            Sprinklers().update_controller_force(
                tag=tag,
                force_water_valve_signal=request.data["force_water_valve_signal"],
                water_valve_signal=request.data["water_valve_signal"],
            )
            return Response({"acknowledge": True}, status=status.HTTP_200_OK)
