"""config URL Configuration

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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from config import settings
from members.views import ObtainTokenView

schema_view = get_schema_view(
    openapi.Info(
        title='MarketBroccoli Backend',
        default_version='v1',
        contact=openapi.Contact(email='sdh5813@gmail.com'),
    ),
    public=True,
)

urlpatterns = [
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0)),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('members.urls'), name='accounts'),
    path('api-token-auth/', ObtainTokenView.as_view(), name='token'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
