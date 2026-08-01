from django.contrib import admin
from django.urls import path, re_path

from tests.testapp.views import HomeView

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    path("admin/", admin.site.urls),
]
