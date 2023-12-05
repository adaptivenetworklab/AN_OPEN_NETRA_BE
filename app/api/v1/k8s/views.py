from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from kubernetes import client, config
from kubernetes.client import configuration
from pick import pick

config.load_kube_config()
v1 = client.CoreV1Api()

@api_view(['GET'])
def endpoints(request):
    routes = [
        '/api/v1/k8s/nodes/',
        '/api/v1/k8s/pods/',
        '/api/v1/k8s/namespaces/',
        '/api/v1/k8s/deployments/',
        '/api/v1/k8s/services/',
        '/api/v1/k8s/namespaces/namespaces-name/pods',

    ]
    return Response(routes)

###k8s - GET PODS###
def GetPods(request):
    if request.method=='GET':
        v1 = client.CoreV1Api() 
        pods_list = v1.list_pod_for_all_namespaces()
    return HttpResponse(pods_list)


###k8s - GET NAMESPACES###
def GetNamespaces(request):
    if request.method=='GET':
        v1 = client.CoreV1Api()       
        ns_list = v1.list_namespace()
    return HttpResponse(ns_list)


###k8s - GET NODES###
def GetNodes(request):
    if request.method=='GET':
        v1 = client.CoreV1Api()
        nodes_list = v1.list_node()
    return HttpResponse(nodes_list)


###k8s - GET DEPLOYMENTS###
def GetDeployments(request):
    if request.method=='GET':
        v1 = client.AppsV1Api() 
        deployments_list: client.V1DeploymentList = v1.list_deployment_for_all_namespaces()
    return HttpResponse(deployments_list)


###k8s - GET SERVICES###
def GetServices(request):
    if request.method=='GET':
        v1 = client.CoreV1Api() 
        services_list = v1.list_service_for_all_namespaces()
    return HttpResponse(services_list)


###k8s - CREATE POD###
# def CreatePod(request):
#     if request.method=='GET':
#         container_name=request.POST.get('container_name')
#         image_name=request.POST.get('image_name')
#         pod_name=request.POST.get('pod_name')
#         namespace_name=request.POST.get('namespace_name')	
#         containers = []
#         container1 = client.V1Container(name='my-nginx-container', image='nginx')
#         containers.append(container1)
#         pod_spec = client.V1PodSpec(containers=containers)
#         pod_metadata = client.V1ObjectMeta(name='my-pod', namespace='default')
#         pod_body = client.V1Pod(api_version='v1', kind='Pod', metadata=pod_metadata, spec=pod_spec)    
#         v1.create_namespaced_pod(namespace='default', body=pod_body)
#     return HttpResponse('Pod successfully created')	
