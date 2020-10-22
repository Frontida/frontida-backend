from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/',include('authentication.urls')),
    path('medical-store/',include('medical_store.urls')),
    path('user/',include('Users.urls'))
]

