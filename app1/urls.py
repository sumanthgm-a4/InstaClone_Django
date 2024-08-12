from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app1 import views

urlpatterns = [
    path("", views.render_home, name="homepage"),
    path("create", views.render_post, name="createpage"),
    path("register", views.render_register, name="registerpage"),
    path("login", views.render_login, name="loginpage"),
    path("logout", views.render_logout, name="logoutpage"),
    path("display/<int:rid>", views.render_display, name="displaypage"),
    path("delete/<int:rid>", views.render_delete, name="delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)