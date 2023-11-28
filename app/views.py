from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Project
from .serializers import ProjectSerializers
from .serializers import UserSerializers

###LANDING PAGE###
@login_required(login_url='login')
@api_view(['GET'])
def landing(request):
    if request.user.is_authenticated:
        return render (request, 'landing.html')
    else:
        return redirect('dashboard')
    

###MAIN - DASHBOARD###
@login_required(login_url='login')
@api_view(['GET'])
def dashboard(request):
    return render (request, 'dashboard.html')


###MAIN - DEPLOY###
@login_required(login_url='login')
@api_view(['GET'])
def deploy(request):
    return render (request, 'deploy.html')


###MAIN - IMAGES###
@login_required(login_url='login')
@api_view(['GET'])
def images(request):
    return render (request, 'images.html')


###MAIN - SERVICES###
@login_required(login_url='login')
@api_view(['GET'])
def services(request):
    return render (request, 'services.html')


###AUTH - SIGNUP###
def SignupPage(request):
    if request.method != 'POST':
        return render (request, 'signup.html')
    email=request.POST.get('email')
    uname=request.POST.get('username')
    pass1=request.POST.get('password1')
    pass2=request.POST.get('password2')

    if pass1 != pass2:
        return HttpResponse('Your password and Confirm Password does not match')
    my_user = User.objects.create_user(uname, email, pass1)
    my_user.save()
    return redirect('login')


###AUTH - LOGIN###
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request, username=username, password=pass1)
        if user is None:
            return HttpResponse('Username or password is incorrect')
        login(request, user)
        return redirect('dashboard')
    return render (request, 'login.html')


###AUTH - LOGOUT###
def LogoutPage(request):
    logout(request)
    return redirect('login')


###ADMIN - USER LIST###
@api_view(['GET', 'POST'])
def user_list(request):
    #Handles GET Request
    if request.method == 'GET':
        #/users/?query=username.value
        query = request.GET.get('query')

        if query is None:
            query = ''

        users = User.objects.filter(username__icontains=query)
        serializer = UserSerializers(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        user = User.objects.create(
            username = request.data['username'],
            password = request.data['password']
        )
        serializer = UserSerializers(user, many=False)
        return Response(serializer.data)


###ADMIN - USER DETAIL###
class UserDetail(APIView):

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist as e:
            raise JsonResponse('Users does not exist') from e

    def get(self, request, username):
        users = self.get_object(username)
        serializer = UserSerializers(users, many=False)
        return Response(serializer.data)
    
    def put(self, request, username):
        users = self.get_object(username)
        users.username = request.data['username']
        users.password = request.data['password']
        users.save()
        serializer = UserSerializers(users, many=False)
        return Response(serializer.data)
    
    def delete(self, request, username):
        users = self.get_object(username)
        users.delete()
        return Response('user successfully deleted')

    
###ADMIN - PROJECT LIST###    
@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all()
    serializer = ProjectSerializers(projects, many=True)
    return Response(serializer.data)

