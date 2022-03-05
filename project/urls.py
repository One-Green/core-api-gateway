"""gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import glbl.views
import sprinkler.views
import water.views
import light.views

schema_view = get_schema_view(
    openapi.Info(
        title="One-Green Core API Gateway ",
        default_version="v1",
        description="Plant cultivation framework",
        terms_of_service="https://github.com/Plant-Keeper/plant-keeper-master/blob/master/LICENSE",
        contact=openapi.Contact(email="shanmugathas.vigneswaran@outlook.fr"),
        license=openapi.License(name="Creative Commons Zero v1.0 Universal"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger views
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Global views
    path("global/config", glbl.views.ConfigView.as_view(), name="global-config"),
    # Sprinklers views
    path(
        "sprinkler/registry",
        sprinkler.views.RegistryView.as_view(),
        name="sprinkler-registry",
    ),
    path(
        "sprinkler/config/<str:tag>",
        sprinkler.views.ConfigView.as_view(),
        name="sprinkler-config",
    ),
    path(
        "sprinkler/controller/force/<str:tag>",
        sprinkler.views.ForceControllerView.as_view(),
        name="sprinkler-force",
    ),
    path(
        "water/registry",
        water.views.RegistryView.as_view(),
        name="water-registry",
    ),
    # Water views
    path("water/config/<str:tag>", water.views.ConfigView.as_view(), name="water-config"),
    path(
        "water/controller/force/<str:tag>",
        water.views.ForceControllerView.as_view(),
        name="water-force",
    ),
    # WIP
    path("light/registry", light.views.RegistryView.as_view(), name="light-registry"),
    path(
        "light/config/<str:tag>", light.views.ConfigView.as_view(), name="light-config"
    ),
    path(
        "light/controller/force/<str:tag>",
        light.views.ForceControllerView.as_view(),
        name="light-force",
    ),
]
