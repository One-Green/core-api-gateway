from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from water.models import Water, ForceController
from water.serializers import ConfigSerializer, ForceControllerSerializer


class ConfigView(GenericAPIView):
    serializer_class = ConfigSerializer

    @csrf_exempt
    def get(self, request):
        """
        Return list of sprinkler tag available on registry
        :param request:
        :return:
        """
        return Response(Water().get_config(), status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        """
        Change water configuration
        :param request:
        :return:
        """
        serializer = ConfigSerializer(data=request.data)
        if serializer.is_valid():
            Water.update_config(
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
    def get(self, request):
        """
        Return list of sprinkler tag available on registry
        :param request:
        :return:
        """
        return Response(Water().get_controller_force(), status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request):
        """
        Change water configuration
        :param request:
        :return:
        """
        serializer = ForceControllerSerializer(data=request.data)
        if serializer.is_valid():
            Water().update_controller_force(
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
