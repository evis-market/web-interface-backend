"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/v1/auth/', include('auth.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/categories/', include('categories.urls')),
    path('api/v1/geo-regions/', include('geo_regions.urls')),
    path('api/v1/sellers/', include('sellers.urls')),
    path('api/v1/seller-products/', include('seller_products.urls')),
    path('api/v1/langs/', include('languages.urls')),
    path('api/v1/shop/', include('shop.urls')),
    path('api/v1/sales', include('sales.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
