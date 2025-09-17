from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('account/', views.account_view, name='account'),
    path('create/', views.create_note_view, name='create_note'),
    path('edit/<uuid:note_id>/', views.edit_note_view, name='edit_note'),
    path('delete/<uuid:note_id>/', views.delete_note_view, name='delete_note'),
]
