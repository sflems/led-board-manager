from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('profiles', views.SettingsView)

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls))
]
