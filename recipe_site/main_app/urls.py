from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('user/', views.user_dashboard_view, name='user_dashboard'),
    path('logout', views.logout_view, name='logout'),
    path('user/recipe/<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail'),
    path('user/recipe/<int:recipe_id>/premade/',views.Premade_recipe_detail_view, name='premade_recipe'),
    path('user/recipe/<int:recipe_id>/edit/', views.edit_recipe_view, name='edit_recipe'),
    path('user/recipe/<int:recipe_id>/deleterecipe/', views.delete_recipe_view, name='delete_recipe'),
    path('user/createrecipe/', views.create_recipe_view, name='create_recipe'),
    path('allrecipes/',views.all_recipes, name='all_recipes'),

]