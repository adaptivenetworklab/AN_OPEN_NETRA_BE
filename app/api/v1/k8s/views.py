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
        contexts, active_context = config.list_kube_config_contexts()
        if not contexts:
            print("Cannot find any context in kube-config file.")
            return
        contexts = [context['name'] for context in contexts]
        active_index = contexts.index(active_context['name'])
        option, _ = pick(contexts, title="Pick the context to load",
                        default_index=active_index)
        # Configs can be set in Configuration class directly or using helper
        # utility
        config.load_kube_config(context=option)

        print(f"Active host is {configuration.Configuration().host}")

        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for item in ret.items:
            print(
                "%s\t%s\t%s" %
                (item.status.pod_ip,
                item.metadata.namespace,
                item.metadata.name))
            
    if __name__ == '__GetPods__':
        GetPods()

###k8s - GET NAMESPACES###
###k8s - GET NODES###
def GetNodes(request):
    if request.method=='GET':
        v1 = client.CoreV1Api()
        list = v1.list_node()
    return HttpResponse(list)
###k8s - GET DEPLOYMENTS###
###k8s - GET SERVICES###



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
