from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from glbl.serializers import ConfigSerializer
from glbl.models import GlobalConfig


class ConfigView(GenericAPIView):
    serializer_class = ConfigSerializer

    @csrf_exempt
    def get(self, request):
        r = GlobalConfig().get_config()
        if r:
            return Response(r, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "configuration not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @csrf_exempt
    def post(self, request):
        serializer = ConfigSerializer(data=request.data)
        if serializer.is_valid():
            if GlobalConfig.update_config(request.data):
                return Response({"acknowledge": True}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"acknowledge": False, "error": "data not accepted"},
                    status=status.HTTP_200_OK,
                )
