from django.contrib import admin
from django.urls import path
from studentorg.views import (
    HomePageView,
    OrganizationList,
    OrganizationCreateView,
    OrganizationUpdateView,
    OrganizationDeleteView,
    StudentList,
    StudentCreateView,
    StudentUpdateView,
    StudentDeleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', HomePageView.as_view(), name='home'),

    # Organization URLs
    path('organization_list/', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add/', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<int:pk>/', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization-delete'),

    # Student list
    path('student_list/', StudentList.as_view(), name='student_list'),
    path('student_list/add/', StudentCreateView.as_view(), name='student-add'),
    path('student_list/<int:pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
]
