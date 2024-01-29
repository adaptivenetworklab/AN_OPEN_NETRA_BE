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
from .k8s_templates import get_role_yaml, get_role_binding_yaml
import subprocess
from app.api.v1.k8s.views import GetPods
from .utils import check_helm_deployment_exists

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
    user_profile = UserProfile.objects.get(user=request.user)
    username = request.session.get('username', 'Unknown User')

    if username == 'admin':
        return render(request, 'admin_dashboard.html')
    else:
        namespace = f"{username}-namespace" 
        single_cu_exists = check_helm_deployment_exists("single-cu", namespace)
        single_du_exists = check_helm_deployment_exists("single-du", namespace)
        single_ru_exists = check_helm_deployment_exists("single-du", namespace)
        single_ue_exists = check_helm_deployment_exists("single-ue", namespace)
        multignb_cu_exists = check_helm_deployment_exists("multignb-cu", namespace)
        multignb_du1_exists = check_helm_deployment_exists("multignb-du1", namespace)
        multignb_du2_exists = check_helm_deployment_exists("multignb-du2", namespace)
        multignb_ru1_exists = check_helm_deployment_exists("multignb-du1", namespace)
        multignb_ru2_exists = check_helm_deployment_exists("multignb-du2", namespace)
        multignb_ue_exists = check_helm_deployment_exists("multignb-ue", namespace)
        multiue_cu_exists = check_helm_deployment_exists("multiue-cu", namespace)
        multiue_du_exists = check_helm_deployment_exists("multiue-du", namespace)
        multiue_ru_exists = check_helm_deployment_exists("multiue-du", namespace)
        multiue_ue1_exists = check_helm_deployment_exists("multiue-ue1", namespace)
        multiue_ue2_exists = check_helm_deployment_exists("multiue-ue2", namespace)


        context = {
            'user_level': user_profile.level,
            'single_cu_exists': single_cu_exists,
            'single_du_exists': single_du_exists,
            'single_ru_exists': single_ru_exists,
            'single_ue_exists': single_ue_exists,
            'multignb_cu_exists': multignb_cu_exists,
            'multignb_du1_exists': multignb_du1_exists,
            'multignb_du2_exists': multignb_du2_exists,
            'multignb_ru1_exists': multignb_ru1_exists,
            'multignb_ru2_exists': multignb_ru2_exists,
            'multignb_ue_exists': multignb_ue_exists,
            'multiue_cu_exists': multiue_cu_exists,
            'multiue_du_exists': multiue_du_exists,
            'multiue_ru_exists': multiue_ru_exists,
            'multiue_ue1_exists': multiue_ue1_exists,
            'multiue_ue2_exists': multiue_ue2_exists
        }
        return render(request, 'user_dashboard.html', context)


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
            created_users = 0  # To count successfully created users

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
                namespace = f'user{i}-namespace'
                role_name = f'user{i}-role'
                role_binding_name = f'user{i}-rolebinding'

                if not User.objects.filter(username=username).exists():
                    new_user = User.objects.create_user(username=username, password=password)
                    UserProfile.objects.create(user=new_user, level=1)
                    
                    # Create the user's namespace
                    subprocess.run(["kubectl", "create", "namespace", namespace])

                    # Generate the role and role binding YAML
                    role_yaml = get_role_yaml(namespace, role_name)
                    role_binding_yaml = get_role_binding_yaml(namespace, role_binding_name, username, role_name)

                    # Apply the role and role binding
                    subprocess.run(["kubectl", "apply", "-f", "-"], input=role_yaml.encode('utf-8'))
                    subprocess.run(["kubectl", "apply", "-f", "-"], input=role_binding_yaml.encode('utf-8'))

                    # Call CreateAll5G with the specific namespace
                    create_5g_result = CreateAll5G(request, namespace)
                    if create_5g_result != "Success":
                        return HttpResponse(create_5g_result)

                    created_users += 1

            return HttpResponse(f"{created_users} users created successfully")
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
    namespace = f"{user.username}-namespace"  # Derive namespace from username

    # Delete user's Kubernetes resources first
    response = DeleteAll5G(request, namespace)

    # If Kubernetes resources deleted successfully, delete the User object
    if response.status_code == 200:
        user.delete()
        return HttpResponse('User and associated resources successfully deleted')
    else:
        return response

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

