from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from studentorg.views import HomePageView
from studentorg import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
]