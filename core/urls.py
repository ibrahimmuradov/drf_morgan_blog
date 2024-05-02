from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('account/', include('account.urls')),
    path('account-api/', include('account.api.urls')),
    # path('blog-api/', include('blog.api.urls')),
    path('contact-api/', include('contact.api.urls'))
]

urlpatterns += i18n_patterns(
    path('blog-api/', include('blog.api.urls')),
)


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


""" SWAGGER TOOLS """
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from services.permissions import AccessPermission

schema_view = get_schema_view(
    openapi.Info(
        title="Morgan Blog Swagger API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(AccessPermission,),
)

urlpatterns += [
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]