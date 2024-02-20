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
import json
import subprocess

config.load_kube_config()

@api_view(['GET'])
def endpoints(request):
    routes = [
        '/api/v1/k8s/nodes',
        '/api/v1/k8s/pods',
        '/api/v1/k8s/namespaces',
        '/api/v1/k8s/deployments',
        '/api/v1/k8s/services',
    ]
    return Response(routes)

###k8s - GET ANNOTATIONS###
def get_network_status_annotations():
    # Load your Kubernetes configuration, either in-cluster or from a local Kubeconfig file
    config.load_kube_config()

    # Initialize the Kubernetes API client
    v1 = client.CoreV1Api()

    # Create a dictionary to hold pod names and their network status in JSON format
    pod_network_status = {}

    # List all pods across all namespaces
    pods = v1.list_pod_for_all_namespaces()

    for pod in pods.items:
        # Ensure annotations are not None
        annotations = pod.metadata.annotations or {}

        # Extract the 'k8s.v1.cni.cncf.io/network-status' annotation
        network_status_str = annotations.get('k8s.v1.cni.cncf.io/network-status')

        if network_status_str:
            try:
                # Parse the network status string as JSON
                network_status_json = json.loads(network_status_str)
                # Store the parsed JSON against the pod's name
                pod_network_status[pod.metadata.name] = network_status_json
            except json.JSONDecodeError:
                # Handle cases where the annotation is not valid JSON
                pod_network_status[pod.metadata.name] = "Invalid JSON or not available"

    return pod_network_status

###k8s - GET PODS###
def GetPods(request):
    if request.method == 'GET':
        config.load_kube_config()
        v1 = client.CoreV1Api()

        # Derive namespace from the current user's username
        user_namespace = f"{request.user.username}-namespace"

        # List pods in the specific namespace
        pods_list = v1.list_namespaced_pod(namespace=user_namespace)

        # Retrieve all network statuses in advance
        network_statuses = get_network_status_annotations()

        # Convert the pods_list to a list of dictionaries
        pods_info = []
        for pod in pods_list.items:
            # Ensure annotations are not None
            annotations = pod.metadata.annotations or {}

            # Retrieve the network status for the current pod
            network_status_json = network_statuses.get(pod.metadata.name, 'Not available')

            pod_info = {
                'name': pod.metadata.name,
                'ip': pod.status.pod_ip,
                'network_status': network_status_json,  # Inserting network status in JSON format
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
        # Load the kubeconfig file
        config.load_kube_config()

        # Create an instance of the API class
        v1 = client.AppsV1Api()

        # Construct the namespace from the current user's username
        user_namespace = f"{request.user.username}-namespace"

        try:
            # List deployments only in the user's namespace
            deployments_list = v1.list_namespaced_deployment(namespace=user_namespace)

            # Convert the deployments_list to a list of deployment names
            deployments = [deployment.metadata.name for deployment in deployments_list.items]

            # Return JsonResponse with the list of deployments
            return JsonResponse({'deployments': deployments})

        except client.exceptions.ApiException as e:
            # Handle the case where the namespace does not exist or other API errors
            return JsonResponse({'error': 'Failed to retrieve deployments', 'details': str(e)}, status=e.status)

    # Handle other HTTP methods if needed
    else:
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


###RELATED TO 5G COMPONENTS MANAGEMENT FEATURE###
###SINGLE CU - RESTART###
def RestartSingleCU(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "single-cu", "--namespace", namespace
        ])
        return HttpResponse("Success")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE DU - RESTART###
def RestartSingleDU(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "single-du", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE UE - RESTART###
def RestartSingleUE(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "single-ue", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB CU - RESTART###
def RestartMultignbCU(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multignb-cu", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU1 - RESTART###
def RestartMultignbDU1(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multignb-du1", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU2 - RESTART###
def RestartMultignbDU2(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multignb-du2", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB UE - RESTART###
def RestartMultignbUE(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multignb-ue", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE CU - RESTART###
def RestartMultiueCU(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multiue-cu", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE DU - RESTART###
def RestartMultiueDU(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"
    
        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multiue-du", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE1 - RESTART###
def RestartMultiueUE1(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multiue-ue1", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE2 - RESTART###
def RestartMultiueUE2(request):
    try:
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        subprocess.run([
            "kubectl", "rollout", "restart", "deployment", "multiue-ue2", "--namespace", namespace
        ])
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MONITORING - LOGS###
def get_pod_logs(pod_name, namespace, since_seconds=1):
    try:
        cmd = [
            "kubectl", "logs", pod_name,
            "-n", namespace,
            "--since={}s".format(since_seconds),
            "--timestamps",
            "--tail=300"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logs = result.stdout.strip().split('\n')
        
        # Initialize an empty list to hold structured logs
        structured_logs = []

        for line in logs:
            parts = line.split()
            # Ensure the line has at least 2 parts
            if len(parts) >= 2:
                timestamp = parts[0]
                log_message = " ".join(parts[1:])
                structured_logs.append({"timestamp": timestamp, "log": log_message})
            else:
                print("Skipping malformed log line:", line)

        return structured_logs
    except subprocess.CalledProcessError as e:
        print("Error fetching logs:", e)
        return []


def pod_logs_view(request, pod_name):
    namespace = request.user.username + "-namespace"  # Assuming namespace is based on the user
    logs = get_pod_logs(pod_name, namespace)
    return JsonResponse(logs, safe=False)  # Use safe=False since we're returning a list