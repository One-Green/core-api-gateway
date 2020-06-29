"""plant_kiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from plant_core import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from plant_kiper import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Plant Keeper API Gateway",
        default_version=settings.__version__,
        description="Still in dev",
        terms_of_service="https://github.com/shanisma/plant-keeper/blob/master/LICENSE",
        contact=openapi.Contact(email="shanmugathas.vigneswara@outlook.fr"),
        license=openapi.License(name="Still in dev"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # url("^$", views.home),
    url(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("admin/", admin.site.urls),
    path("api-v1/enclosure/", views.EnclosureView.as_view()),
    path("api-v1/sprinkler/", views.SprinklerView.as_view()),
    path("api-v1/water/", views.WaterView.as_view()),
    path("api-v1/heater/", views.HeaterView.as_view()),
    path("api-v1/cooler/", views.CoolerView.as_view()),
    path("api-v1/air-humidifier/", views.AirHumidifierView.as_view()),
]
