from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . models import CustomRecipe, PremadeRecipe, WeeklyMealPlan

# Create your views here.
def home(request):
    return render(request, 'main_app/homepage.html')


def login_view(request):
    if request.method == 'POST':
        # login logic here
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f'User: {username} logged in successfully')
            # Redirect user back to the same login page (user doesn't go anywhere)
            return HttpResponseRedirect(reverse('user_page'))
        else:
            print(f'Invalid login attempt with username: {username}')
            # Return an 'invalid login' error message
            return render(request, 'main_app/login.html', {
                'error_msg': 'Invalid username or password'})
    
    # Render the login form
    return render(request, 'main_app/login.html')

def signup_view(request):
    if request.method == 'POST':
        # signup logic here
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            print('Passwords do not match')
            return render(request, 'main_app/signup.html', {
                'error_msg': 'Passwords do not match. Please try again.'})
        if len(password) < 3:
            print('Password is too short')
            return render(request, 'main_app/signup.html', {
                'error_msg': 'Password must be at least 3 characters long.'})
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            print('Username already exists')
            return render(request, 'main_app/signup.html', {
                'error_msg': 'Username already exists. Please choose a different one.'})
        
        # If we passed all conditions, then we can create a new user!
        print('Username is available')

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        print(f'User: {username} signed up successfully')

        # Redirect user back to login page to sign in 
        return HttpResponseRedirect(reverse('login'))
    
    return render(request, 'main_app/signup.html')

def user_page(request):
    if not request.user.is_authenticated:
        print('user not authenticated')
        return HttpResponseRedirect(reverse('login'))
    else:
        print(f'User: {request.user.username} is authenticated')
        print([recipe for recipe in request.user.custom_recipes.all()])
        return render(request, 'main_app/user.html', {
            'user': request.user,
            'custom_recipes': request.user.custom_recipes.all(),
        })
    
def logout_view(request):
    logout(request)
    return render(request, 'main_app/homepage.html', {
        'logout_msg' : 'You have been logged out.'
    })

def recipe_detail(request, recipe_id):

    recipe_exists = CustomRecipe.objects.filter(id=recipe_id).exists()
    recipe_is_users = CustomRecipe.objects.filter(id=recipe_id, user=request.user).exists()
 
    if not request.user.is_authenticated:
        print('user not authenticated')
        return HttpResponseRedirect(reverse('login'))
    
    elif not recipe_exists:
        print(f'Recipe with ID {recipe_id} does not exist')
        # redirects user back to their user page if the recipe does not exist
        # this is primarily when the user tried to access a recipe by 
        # manually entering the URL /recipe/<recipe_id_that_doesn't_exist>
        return HttpResponseRedirect(reverse('user_page'))
    
    elif not recipe_is_users:
        print(f'User: {request.user.username} is authenticated and but is NOT the owner of the recipe')
        # Get the recipe object
        return HttpResponseRedirect(reverse('user_page'))

    else:

        print(f'User: {request.user.username} is authenticated and IS the owner of the recipe!')
        print(f'{CustomRecipe.objects.filter(id=recipe_id)}')
        return render(request, 'main_app/recipe.html', {
            'recipe': CustomRecipe.objects.filter(id=recipe_id).first(),
        })