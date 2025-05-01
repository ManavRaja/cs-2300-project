from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('user/', views.user_page, name='user_page'),
    path('logout', views.logout_view, name='logout'),
    path('user/recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]