from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . models import CustomRecipe, PremadeRecipe, WeeklyMealPlan
from .forms import RecipeForm 



# Create your views here.
def home_view(request):
    """
    View function to handle the homepage rendering.
    """
    
    return render(request, 'main_app/homepage.html')



def login_view(request):
    """
    View function to handle user login.
    - Renders the login form on GET request.
    - Processes submitted form data on POST request.
    - Authenticates the user and logs them in if valid.
    - Redirects to the user dashboard upon successful login.
    - Displays an error message for invalid login attempts.
    - If the user is already authenticated, redirects to the user dashboard.
    """
    
    if request.method == 'POST':
        # login logic here
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f'User: {username} logged in successfully')
            # Redirect user back to the same login page (user doesn't go anywhere)
            return HttpResponseRedirect(reverse('user_dashboard'))
        else:
            print(f'Invalid login attempt with username: {username}')
            # Return an 'invalid login' error message
            return render(request, 'main_app/login.html', {
                'error_msg': 'Invalid username or password'})
    else:
        # If it's a GET request, render the login form
        print('GET request for login page')
        # Check if the user is already authenticated
        if request.user.is_authenticated:
            print(f'User: {request.user.username} is already authenticated')
            # Redirect to the user dashboard if already logged in
            return redirect('user_dashboard')   
        else:
            # Render the login form
            return render(request, 'main_app/login.html')



def signup_view(request):
    """
    View function to handle user signup.

    - Renders the signup form on GET request.
    - Processes submitted form data on POST request.
    - Validates the form data and creates a new user if valid.
    - Redirects to the login page upon successful signup.
    """

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



def user_dashboard_view(request):
    """
    View function to handle displaying the user dashboard.

    - Ensures the user is authenticated before accessing this view.
    - If the user is not authenticated, redirects them to the login page.
    - If the user is authenticated, retrieves their custom recipes
    and renders the user dashboard template.
    """
    
    if not request.user.is_authenticated:
        print('user not authenticated')
        return HttpResponseRedirect(reverse('login'))
    else:
        print(f'User: {request.user.username} is authenticated')
        print([recipe for recipe in request.user.custom_recipes.all()])
        return render(request, 'main_app/user.html', {
            'user': request.user,
            'custom_recipes': request.user.custom_recipes.all()
        })
    


def logout_view(request):
    logout(request)
    return render(request, 'main_app/homepage.html', {
        'logout_msg' : 'You have been logged out.'
    })



def recipe_detail_view(request, recipe_id):
    """
    View function to handle displaying a custom recipe.

    - Ensures the user is authenticated and owns the recipe.
    - If the recipe does not exist or the user is not the owner,
    redirects them to the user dashboard.
    """

    # Before doing anything, check if the user is authenticated
    # If not, redirect them to the login page
    if not request.user.is_authenticated:
        print('User not authenticated')
        return HttpResponseRedirect(reverse('login'))
    
    # Get vars indicating if recipe exists and if the user is the owner
    recipe_exists = CustomRecipe.objects.filter(id=recipe_id).exists()
    recipe_is_users = CustomRecipe.objects.filter(id=recipe_id, user=request.user).exists()
    
    # Check if the recipe exists and if the user is the owner
    if not recipe_exists:
        print(f'Recipe with ID {recipe_id} does not exist')
        # redirects user back to their user page if the recipe does not exist
        # this is primarily when the user tried to access a recipe by 
        # manually entering the URL /recipe/<recipe_id_that_doesn't_exist>
        return HttpResponseRedirect(reverse('user_dashboard'))
    
    elif not recipe_is_users:
        print(f'User: {request.user.username} is authenticated but is NOT the owner of the recipe')
        return HttpResponseRedirect(reverse('user_dashboard'))

    else:
        print(f'User: {request.user.username} is authenticated and IS the owner of the recipe!')
        print(f'{CustomRecipe.objects.filter(id=recipe_id)}')
        return render(request, 'main_app/recipe.html', {
            'recipe': CustomRecipe.objects.filter(id=recipe_id).first(),
        })

    

def edit_recipe_view(request, recipe_id):
    """
    View function to handle editing an existing custom recipe.

    - Ensures the user owns the recipe and uses RecipeForm correctly.
    - Also handles when user tries to edit a recipe's name to one that already exists FOR THEM.
    """
    # Get the recipe object or return a 404 error if not found
    recipe = get_object_or_404(CustomRecipe, pk=recipe_id)

    # Check if the logged-in user owns this recipe.
    if recipe.user != request.user:
        # redirect to user dashboard b/c user cannot edit other people's recipes
        print(f'User: {request.user.username} attempted to edit recipe {recipe_id} owned by {recipe.user.username}')
        return redirect('user_dashboard') 

    if request.method == 'POST':
        # If the form was submitted, bind the POST data and files to the form,
        # specifying the instance to update the existing recipe.
        form = RecipeForm(request.POST, request.FILES, instance=recipe, user=request.user)
        if form.is_valid():
            # Form validation 
            # check for the (user, name) uniqueness constraint
            try:
                form.save() # Save the changes to the database
                # Redirect to the recipe detail page after successful edit
                return redirect('recipe_detail', recipe_id=recipe.id)
            
            except ValueError as e: # Catch potential errors from form.save()
                 form.add_error(None, str(e))

            except Exception as e: # Catch other potential saving errors
                 print(f"Error updating recipe {recipe_id}: {e}") # Log the error
                 form.add_error(None, "Already have a recipe with that name.") # Add error to form

    else:
        # If GET request create a form instance 
        # populated with the existing recipe data 
        form = RecipeForm(instance=recipe, user=request.user)

    # Pass this info to template
    context = {
        'form': form,
        'recipe': recipe #recipe object
    }
    # Render the template used for editing recipes.
    return render(request, 'main_app/edit_recipe.html', context)



def delete_recipe_view(request, recipe_id):
    """
    View function to handle deleting a custom recipe.

    - If the recipe does not exist return a 404 error.
    - If the user is not the owner, redirects them to the user dashboard.
    - If the user is the owner and the request method is POST, delete the recipe.
    - Redirects to the user dashboard after deletion.
    """

    # Get the recipe object or return a 404 error if not found
    recipe = get_object_or_404(CustomRecipe, pk=recipe_id)
    # Optional: Check if the logged-in user owns this recipe if necessary
    if recipe.user != request.user:
        # Unauthorized access
        print(f'User: {request.user.username} is authenticated but is NOT the owner of the recipe')
        return redirect('user_dashboard')

    if request.method == 'POST':
        # If the form was submitted, delete the recipe
        recipe.delete()
        # Redirect to the user page after successful deletion
        return redirect('user_dashboard')
    else:
        print(f'User: {request.user.username} is authenticated and IS the owner of the recipe BUT its not a POST request!')
        return redirect('user_dashboard')



def create_recipe_view(request):
    """
    View function to handle the creation of a new custom recipe.

    - Renders the recipe form on GET request.
    - Processes submitted form data on POST request.
    - Uses RecipeForm which associates the new recipe with the logged in user before saving.
    - Redirects to the new recipe's detail page upon successful creation.
    - Handles form validation and error display.
    """
    if request.method == 'POST':
        # If the form was submitted, bind the POST data and files to the form
        # Pass the logged-in user to the form's constructor
        form = RecipeForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            try:
                # Directly call form.save() which handles user assignment and commit
                new_recipe = form.save()
                # Redirect to the detail page of the newly created recipe
                return redirect('recipe_detail', recipe_id=new_recipe.id) 
            
            except ValueError as e:
                # Handle errors from form.save()
                form.add_error(None, str(e)) # Adds error to display it at top of the form

            except Exception as e:
                # Catch other potential erros not from form validation
                print(f"Error saving recipe: {e}")
                form.add_error(None, "Already have a recipe with that name.") # Add error to form

    else:
        # If it's a GET request, create a form instance.
        form = RecipeForm(user=request.user)

    # Info to pass into template
    context = {
        'form': form
    }
    # Render the template used for creating recipes.
    return render(request, 'main_app/create_recipe.html', context)