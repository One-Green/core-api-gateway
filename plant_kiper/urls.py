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
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Plant Keeper API')

urlpatterns = [
    url(r'^$', schema_view),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('admin/', admin.site.urls),
    path('enclosure/', views.EnclosureView.as_view()),
    path('cooler/', views.CoolerView.as_view()),
    path('vaporgenerator/', views.VaporGeneratorView.as_view()),
    path('watertank/', views.WaterTankView.as_view()),
    path('heater/', views.HeaterView.as_view()),
    path('uvlight/', views.UvLightView.as_view()),
    path('co2valve/', views.CO2ValveView.as_view()),
    path('filters/', views.FiltersView.as_view())
]
