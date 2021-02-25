from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from water.models import Water
from water.serializers import ConfigSerializer


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
