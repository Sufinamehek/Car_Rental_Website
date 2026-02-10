
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']

#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists')
#             return redirect('signup')

#         User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )
#         messages.success(request, 'Account created successfully')
#         return redirect('login')

#     return render(request, 'accounts/signup.html')


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('login')  # later redirect to car list
#         else:
#             messages.error(request, 'Invalid credentials')

#     return render(request, 'accounts/login.html')


# def logout_view(request):
#     logout(request)
#     return redirect('login')
#  authenticate, login, logout


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')

    return render(request, 'accounts/signup.html')


def logout_view(request):
    logout(request)
    return redirect('accounts/login.html')
