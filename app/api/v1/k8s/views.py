from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from kubernetes import client, config
from kubernetes.client import configuration
from pick import pick

config.load_kube_config()
v1 = client.CoreV1Api()

@api_view(['GET'])
def endpoints(request):
    routes = [
        '/api/v1/k8s',
        '/api/token/refresh',
        '/api/my-api'
    ]
    return Response(routes)

###K8S - CREATE POD###
@login_required(login_url='login')
def CreatePod(request):
    if request.method=='GET':
        container_name=request.POST.get('container_name')
        image_name=request.POST.get('image_name')
        pod_name=request.POST.get('pod_name')
        namespace_name=request.POST.get('namespace_name')	
        containers = []
        container1 = client.V1Container(name='my-nginx-container', image='nginx')
        containers.append(container1)
        pod_spec = client.V1PodSpec(containers=containers)
        pod_metadata = client.V1ObjectMeta(name='my-pod', namespace='default')
        pod_body = client.V1Pod(api_version='v1', kind='Pod', metadata=pod_metadata, spec=pod_spec)    
        v1.create_namespaced_pod(namespace='default', body=pod_body)
    return HttpResponse('Pod successfully created')	
