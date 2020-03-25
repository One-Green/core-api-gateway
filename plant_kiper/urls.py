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
from .settings import __version__

schema_view = get_schema_view(
    openapi.Info(
        title='Plant Keeper API Gateway',
        default_version=__version__,
        description="Still in dev",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shanmugathas.vigneswara@outlook.fr"),
        license=openapi.License(name="Still in dev"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('enclosure/', views.EnclosureView.as_view()),
    path('cooler/', views.CoolerView.as_view()),
    path('air-humidifier/', views.AirHumidifierView.as_view()),
    path('water-pump/', views.WaterPumpView.as_view()),
    path('sprinkler-valve/', views.SprinklerValveView.as_view()),
    path('heater/', views.HeaterView.as_view()),
    path('uv-light/', views.UvLightView.as_view()),
    path('co2-valve/', views.CO2ValveView.as_view()),
    path('filters/', views.FiltersView.as_view())
]
