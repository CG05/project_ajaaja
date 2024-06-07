from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index),
    path("account/login/", views.login, name='login'),
    path("account/logout/", views.logout, name='logout'),
    path("account/register/", views.createAccount, name="create"),
    path("page/", include("page.urls")),
    path("utab/", include("utab.urls")),
    path("ltab/", include("ltab.urls")),
    path('notion/', include('notion.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
