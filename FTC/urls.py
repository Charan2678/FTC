from django.urls import include, re_path 
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

urlpatterns = [
    re_path(r'^', include('pages.urls')),
    re_path(r'^company/', include('company.urls')),
    re_path(r'^type/', include('type.urls')),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^products/', include('products.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include('products.urls')),  # API endpoints
    re_path(r'^database-dashboard/$', lambda request: render(request, 'database_dashboard.html'), name='database_dashboard'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
