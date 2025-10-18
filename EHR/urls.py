from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from two_factor.urls import urlpatterns as tf_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('account.urls')),
    path('', include(tf_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

