from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from root.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

admin.site.index_title = _('My Index Title')
admin.site.site_header = _('Alijahon Administration')
admin.site.site_title = _('My Site Management')
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("", include('apps.urls')),
    prefix_default_language=True
) + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)
