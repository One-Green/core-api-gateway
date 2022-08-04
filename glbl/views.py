from glbl.serializers import ConfigSerializer
from glbl.models import Config
from rest_framework.viewsets import ModelViewSet


class ConfigView(ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    search_fields = ["site_tag"]
