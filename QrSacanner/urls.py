from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', register_user, name='register_user'),
    path('user_profile/<int:user_id>/', user_profile, name='user_profile'),
    # path('scan/', scan_qr_code, name='scan_qr_code'),
    # path('process_qr/', process_qr, name='process_qr'),
    path('user_data/<int:user_id>/', user_data_api, name='user_data_api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
