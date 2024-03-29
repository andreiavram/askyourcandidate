from django.conf import settings
from django.urls import re_path as url, include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^login/$', auth_views.LoginView.as_view(), name="login"),
    url('^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url('^change-password/$', auth_views.PasswordChangeView.as_view(), name="change_password"),
    url('^password-change-done/$', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('', include('questions.urls', namespace="questions")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
