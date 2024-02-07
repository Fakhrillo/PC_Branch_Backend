from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("core.urls")),
    path("api/docs/", include_docs_urls(title="API Docs")),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
