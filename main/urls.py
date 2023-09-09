from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('delete/<int:pk>/', views.BoxDeleteView.as_view(), name='box-delete'),
    path('register/', views.RegisterUser.as_view(), name='register_user'),
    path('login/', views.CustomLoginView.as_view(), name='login_user'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('list/', views.BoxListView.as_view(), name="box_list"),
    path('create/', views.BoxCreateView.as_view(), name='box-create'),
    path('update/<int:pk>/', views.BoxUpdateView.as_view(), name='box-update'),  # Add this line
]