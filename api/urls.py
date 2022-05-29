from django.urls import path
from .views import UserCreate, create_like, UserListView



urlpatterns = [
    path('clients/create', UserCreate.as_view(), name='user_create'),
    path('clients/<int:pk>/match', create_like, name='create_like'),
    path('list', UserListView.as_view(), name='user_list')

]
