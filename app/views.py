from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from app.api.v1.oai.views import CreateAll5G, DeleteAll5G
from .models import UserProfile 
import re

###PAGES - REVERSE###
@login_required(login_url='login')
@api_view(['GET'])
def reverse(request):
    # Redirect to the dashboard view
    return redirect('dashboard')
    

###PAGES - INTRODUCTION###
@login_required(login_url='login')
@api_view(['GET'])
def introduction(request):
    # Retrieve the username from the session
    username = request.session.get('username', 'Unknown User')
    if username == 'admin':
        return render(request, 'admin_introduction.html', {'username': username})
    else:
        return render(request, 'user_introduction.html', {'username': username})


###PAGES - DASHBOARD###
@login_required(login_url='login')
def dashboard(request):
    # Retrieve the username from the session
    username = request.session.get('username', 'Unknown User')
    if username == 'admin':
        return render(request, 'admin_dashboard.html', {'username': username})
    else:
        return render(request, 'user_dashboard.html', {'username': username})


###PAGES - USER MANAGEMENT & LIST USER###
@login_required(login_url='login')
def UserManagement(request):
    user_data = []

    for user in User.objects.filter(is_superuser=False):
        profile, created = UserProfile.objects.get_or_create(user=user)
        user_data.append({
            'user': user,
            'level': profile.level
        })

    return render(request, 'user_management.html', {'user_data': user_data})


###PAGES - MONITORING###
@login_required(login_url='login')
def monitoring(request):
    # Retrieve the username from the session
    username = request.session.get('username', 'Unknown User')
    if username == 'admin':
        return render(request, 'admin_monitoring.html', {'username': username})
    else:
        return render(request, 'user_monitoring.html', {'username': username})


###USER - CREATE A NEW USER###
@login_required(login_url='login')
def CreateUser(request):
    if request.method == 'POST':
        try:
            user_count = int(request.POST.get('user_count', 1))
            user_count = max(user_count, 1)  # Ensure at least one user is created

            highest_number = 0

            # Find the highest existing username number
            for user in User.objects.filter(username__startswith='user'):
                match = re.match(r'user(\d+)', user.username)
                if match:
                    number = int(match.group(1))
                    highest_number = max(highest_number, number)

            # Start creating users from the next available number
            for i in range(highest_number + 1, highest_number + user_count + 1):
                username = f'user{i}'
                password = f'user{i}'
                if not User.objects.filter(username=username).exists():
                    new_user = User.objects.create_user(username=username, password=password)
                    UserProfile.objects.create(user=new_user, level=1)
                    return CreateAll5G(request)

            return HttpResponse(f"{user_count} users created successfully")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
    else:
        return render(request, 'create_user.html')


###USER - UPDATE USER###
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)  # Ensure only superusers can update users
def UpdateUser(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST.get('password')

        user.username = username
        if password:
            user.set_password(password)
        user.save()

        return redirect('user-management')  # Redirect to user management page

    return render(request, 'update_user.html', {'user': user})


###USER - DELETE USER###
@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def DeleteUser(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return DeleteAll5G(request)


###AUTH - LOGIN###
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            # Store the username in the session
            request.session['username'] = username
            return redirect('introduction')
        else:
            return HttpResponse('Username or password is incorrect')

    return render(request, 'login.html')


###AUTH - LOGOUT###
def LogoutPage(request):
    logout(request)
    return redirect('login')

