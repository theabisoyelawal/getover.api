from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from tasks.views import RegisterView, TaskViewSet, UserViewSet

# Customizing the Router Title
class GetOverRouter(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        root_view = super().get_api_root_view(api_urls=api_urls)
        root_view.cls.__doc__ = "Welcome to the GetOver Task Management API"
        return root_view

# Initialize your custom router
router = GetOverRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This will now show the customized root
    path('', include(router.urls)),
    
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', obtain_auth_token, name='login'),
    path('api/', include(router.urls)),
    
    # This enables the "Log out" button in the top right to work correctly
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]