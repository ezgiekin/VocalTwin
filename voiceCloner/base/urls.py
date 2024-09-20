from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import VoiceRecordingViewSet,AudioFileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = 'base'

# DRF Router for API endpoints
router = DefaultRouter()
router.register(r'voice-recordings', VoiceRecordingViewSet)
router.register(r'audio-files', AudioFileViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Voice Cloning API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


urlpatterns = [
    # Traditional Django views
    path('', views.opening, name='opening'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login'),
    path('record_delete/<int:id>', views.delete_object_function, name='delete_object'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('record_voice/', views.record_voice, name='record_voice'),
    path('clone_voice/<int:id>', views.clone, name='clone'),
    path('add_record/<int:id>', views.add_record, name='add_record'),
    path('result/<int:id>', views.result, name='result'),
    path('logout/', views.logout, name='logout'),

    # DRF API endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/clone-voice/<int:id>/', views.clone_voice_api, name='clone_voice_api'),
    path('api/add-audio/<int:id>/', views.add_audio_to_record, name='add_audio_to_record'),

        # Swagger schema views
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
]