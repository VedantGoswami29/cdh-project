from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def _login(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            msg = f"Login Successfully & Redirected to '{next}'" if next!='/' else "Login Successfully"
            messages.success(request, msg)
            return redirect(f"{next}")
        messages.error(request, 'Invalid login credentials')
        return redirect('/login')
    else:
        return render(request, 'login.html')


def _logout(request):
    user = request.user
    logout(request)
    messages.error(request, f"{user.first_name} Logout Successfully")
    return redirect('/')


def index(request):
    return render(request, 'index.html')


