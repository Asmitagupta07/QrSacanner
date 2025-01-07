from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', register_user, name='register_user'),
    path('user_profile/<int:id>/', user_profile, name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
