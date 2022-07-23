from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logged_out.html"), name="logout"),
    path("api/", include("api.urls")),
    # Company Data
    path("company_data/", views.company_data, name="company_data"),
    path("company_data/<path:path>", views.company_data),
    # Program Data
    path("programs/", views.programs, name="programs"),
    path("programs/<path:path>", views.programs),
    # Default Data
    path("colors/", views.colors, name="colors"),
    path("colors/<path:path>", views.colors, name="colors"),
    path("admin/", admin.site.urls),
]
