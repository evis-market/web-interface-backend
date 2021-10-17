from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from app.conf.base import MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('api/v1/shop/', include('shop.urls')),
    path('api/v1/auth/', include('auth.urls')),
    path('api/v1/health_check/', include('health_check.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/sellers/', include('sellers.urls')),
    path('api/v1/seller_products/', include('seller_products.urls')),
    path('api/v1/sales/', include('sales.urls')),
    path('api/v1/categories/', include('categories.urls')),
    path('api/v1/geo-regions/', include('geo_regions.urls')),
    path('api/v1/langs/', include('languages.urls')),
    path('api/v1/upload/', include('upload.urls')),
    path('admin/', admin.site.urls),
] + static(
    MEDIA_URL, document_root=MEDIA_ROOT
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
