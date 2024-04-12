from django.urls import path
from .views import SignupAPIView, LoginAPIView, AddUserDetailsAPIView, UpdateUserProfileAPIView, DeleteUserAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('add-user-details/', AddUserDetailsAPIView.as_view(), name='add_user_details'),
    path('update-user-profile/', UpdateUserProfileAPIView.as_view(), name='update_user_profile'),
    path('delete-user/', DeleteUserAPIView.as_view(), name='delete_user'),
]
