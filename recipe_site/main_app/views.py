from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, 'main_app/homepage.html')

def login(request):
    return render(request, 'main_app/login.html')

def signup(request):
    return render(request, 'main_app/signup.html')