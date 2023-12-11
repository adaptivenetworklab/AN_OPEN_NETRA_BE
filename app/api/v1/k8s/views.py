from importlib import metadata
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
# def GetPods(request):
#     if request.method == 'GET':
#         v1 = client.CoreV1Api()
#         pods_list = v1.list_pod_for_all_namespaces()

#         # Convert the pods_list to a dictionary
#         pods_dict = {}
#         for pod in pods_list.items:
#             pods_dict[pod.metadata.name] = {
#                 'namespace': pod.metadata.namespace,
#                 'status': pod.status.phase,
#                 # Add more fields as needed
#             }

#         # Return JsonResponse with the pods_dict
#         return JsonResponse(pods_dict)

#     # Handle other HTTP methods if needed
#     return HttpResponse("Method not allowed", status=405)
def GetPods(request):
    if request.method == 'GET':
        v1 = client.CoreV1Api()
        pods_list = v1.list_pod_for_all_namespaces()

        # Convert the pods_list to a list of dictionaries
        pods_info = []
        for pod in pods_list.items:
            pod_info = {
                'name': pod.metadata.name,
                'ip': pod.status.pod_ip,
                #'interface': pod.spec.containers[0].interface,  # Adjust based on your container configuration
                'state': pod.status.phase,
                'namespace': pod.metadata.namespace,
                'node': pod.spec.node_name,
                # Add more fields as needed
            }
            pods_info.append(pod_info)

        # Return JsonResponse with the list of pod information
        return JsonResponse({'pods': pods_info})

    # Handle other HTTP methods if needed
    return HttpResponse("Method not allowed", status=405)

###k8s - GET NAMESPACES###
def GetNamespaces(request):
    if request.method == 'GET':
        v1 = client.CoreV1Api()
        ns_list = v1.list_namespace()

        # Convert the ns_list to a list of namespace names
        namespaces = [ns.metadata.name for ns in ns_list.items]

        # Return JsonResponse with the list of namespaces
        return JsonResponse({'namespaces': namespaces})

    # Handle other HTTP methods if needed
    return HttpResponse("Method not allowed", status=405)


###k8s - GET NODES###
def GetNodes(request):
    if request.method == 'GET':
        v1 = client.CoreV1Api()
        nodes_list = v1.list_node()

        # Convert the nodes_list to a list of node names
        nodes = [node.metadata.name for node in nodes_list.items]

        # Return JsonResponse with the list of nodes
        return JsonResponse({'nodes': nodes})

    # Handle other HTTP methods if needed
    return HttpResponse("Method not allowed", status=405)


###k8s - GET DEPLOYMENTS###
def GetDeployments(request):
    if request.method == 'GET':
        v1 = client.AppsV1Api()
        deployments_list = v1.list_deployment_for_all_namespaces()

        # Convert the deployments_list to a list of deployment names
        deployments = [deployment.metadata.name for deployment in deployments_list.items]

        # Return JsonResponse with the list of deployments
        return JsonResponse({'deployments': deployments})

    # Handle other HTTP methods if needed
    return HttpResponse("Method not allowed", status=405)


###k8s - GET SERVICES###
def GetServices(request):
    if request.method == 'GET':
        v1 = client.CoreV1Api()
        services_list = v1.list_service_for_all_namespaces()

        # Convert the services_list to a list of service names
        services = [service.metadata.name for service in services_list.items]

        # Return JsonResponse with the list of services
        return JsonResponse({'services': services})

    # Handle other HTTP methods if needed
    return HttpResponse("Method not allowed", status=405)


###k8s - CREATE POD###
def CreatePod(request):
    if request.method=='POST':
        v1 = client.CoreV1Api()
        container_name=request.POST.get('container')
        image_name=request.POST.get('image')
        pod_name=request.POST.get('pod')
        namespace_name=request.POST.get('namespace')	
        containers = []
        container1 = client.V1Container(name=container_name, image=image_name)
        containers.append(container1)
        pod_spec = client.V1PodSpec(containers=containers)
        pod_metadata = client.V1ObjectMeta(name=pod_name, namespace=namespace_name)
        pod_body = client.V1Pod(api_version='v1', kind='Pod', metadata=pod_metadata, spec=pod_spec)    
        v1.create_namespaced_pod(namespace='default', body=pod_body)
        return HttpResponse('Pod successfully created')
    return render (request, 'create_pod.html')
    	

###k8s - CREATE NAMESPACE###
def CreateNamespace(request):
    if request.method=='POST':
        v1 = client.CoreV1Api()
        name=request.POST.get('namespace')
        namespace_name=client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
        v1.create_namespace(namespace_name)
        return HttpResponse('Namespace successfully created')
    return render (request, 'create_ns.html')

###k8s - CREATE DEPLOYMENTS###
