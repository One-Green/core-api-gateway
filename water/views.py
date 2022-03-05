from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from core.utils import get_now
from water.models import Water, Device
from water.serializers import (
    ConfigSerializer,
    ForceControllerSerializer,
    DeviceSerializer,
)


class DeviceView(GenericAPIView):
    serializer_class = DeviceSerializer

    @csrf_exempt
    def get(self, request):
        """
        Return list of sprinkler tag available on registry
        :param request:
        :return:
        """
        r = Device.objects.values_list("tag", flat=True)
        return Response(r, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        """
        Add new sprinkler tag on registry
        :param request:
        :return:
        """
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            tag = request.data["tag"]
            print(
                f"[{get_now()}] [INFO] "
                f"New Water with {tag=} "
                f"want to register ..."
            )
            if Water().is_tag_in_registry(tag):
                r = {"acknowledge": False}
                print(
                    f"[{get_now()}] [WARNING] "
                    f"This tag {tag=} is already in registry"
                )
            else:
                r = {"acknowledge": True}
                Water().add_tag_in_registry(tag)
                print(f"[{get_now()}] [OK] " f"New Water with {tag=} ")
            return Response(r, status=status.HTTP_200_OK)

    @csrf_exempt
    def delete(self, request):
        try:
            Device.objects.get(tag=request.data["tag"]).delete()
            return Response({"acknowledge": True}, status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({"acknowledge": False}, status=status.HTTP_404_NOT_FOUND)


class ConfigView(GenericAPIView):
    serializer_class = ConfigSerializer

    @csrf_exempt
    def get(self, request, tag):
        """
        Return list of sprinkler tag available on registry
        :param tag:
        :param request:
        :return:
        """
        return Response(Water().get_config(tag), status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, tag):
        """
        Change water configuration
        :param tag:
        :param request:
        :return:
        """
        serializer = ConfigSerializer(data=request.data)
        if serializer.is_valid():
            Water.update_config(
                tag=tag,
                ph_min_level=request.data["ph_min_level"],
                ph_max_level=request.data["ph_max_level"],
                tds_min_level=request.data["tds_min_level"],
                tds_max_level=request.data["tds_max_level"],
            )
            return Response({"acknowledge": True}, status=status.HTTP_200_OK)


class ForceControllerView(GenericAPIView):
    """
    For debug only, force actuator status
    """

    serializer_class = ForceControllerSerializer

    @csrf_exempt
    def get(self, request, tag):
        """
        Return list of sprinkler tag available on registry
        :param tag:
        :param request:
        :return:
        """
        return Response(Water().get_controller_force(tag), status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, tag):
        """
        Change water configuration
        :param tag:
        :param request:
        :return:
        """
        serializer = ForceControllerSerializer(data=request.data)
        if serializer.is_valid():
            Water().update_controller_force(
                tag=tag,
                force_water_pump_signal=request.data["force_water_pump_signal"],
                force_nutrient_pump_signal=request.data["force_nutrient_pump_signal"],
                force_ph_downer_pump_signal=request.data["force_ph_downer_pump_signal"],
                force_mixer_pump_signal=request.data["force_mixer_pump_signal"],
                water_pump_signal=request.data["water_pump_signal"],
                nutrient_pump_signal=request.data["nutrient_pump_signal"],
                ph_downer_pump_signal=request.data["ph_downer_pump_signal"],
                mixer_pump_signal=request.data["mixer_pump_signal"],
            )
            return Response({"acknowledge": True}, status=status.HTTP_200_OK)
