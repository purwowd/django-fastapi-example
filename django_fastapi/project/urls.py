from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles import views

urlpatterns = [path("admin/", admin.site.urls)]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    from django.urls import re_path

    urlpatterns += [re_path(r"^static/(?P<path>.*)$", views.serve)]
