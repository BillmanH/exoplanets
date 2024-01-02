from django.contrib import admin
from django.urls import include, path
from ms_identity_web.django.msal_views_and_urls import MsalViews
from django.conf.urls.static import static
from django.conf import settings


msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()


urlpatterns = [
    path('/', include('app.urls')),
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/',views.signup),

    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    
]