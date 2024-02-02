from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import subprocess
import yaml
import os
from app.models import UserProfile
from django.views.decorators.csrf import csrf_exempt


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Default BASE_DIR located at v1 directory

SINGLE_CU_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-e2e/oai-cu')  # Adjust 'subdirectory' as needed
SINGLE_DU_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-e2e/oai-du')  # Adjust 'subdirectory' as needed
SINGLE_UE_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-e2e/oai-nr-ue')  # Adjust 'subdirectory' as needed

MULTI_GNB_CU_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-gnb/oai-cu')  # Adjust 'subdirectory' as needed
MULTI_GNB_DU1_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-gnb/oai-du-1')  # Adjust 'subdirectory' as needed
MULTI_GNB_DU2_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-gnb/oai-du-2')  # Adjust 'subdirectory' as needed
MULTI_GNB_UE_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-gnb/oai-nr-ue')  # Adjust 'subdirectory' as needed

MULTI_UE_CU_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-ue/oai-cu')  # Adjust 'subdirectory' as needed
MULTI_UE_DU_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-ue/oai-du')  # Adjust 'subdirectory' as needed
MULTI_UE_UE1_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-ue/oai-nr-ue-1')  # Adjust 'subdirectory' as needed
MULTI_UE_UE2_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-multi-ue/oai-nr-ue-2')  # Adjust 'subdirectory' as neededCU1_VALUES_FILE_PATH = os.path.join(CU1_BASE_DIR, 'values.yaml')

SINGLE_CU_VALUES_FILE_PATH = os.path.join(SINGLE_CU_BASE_DIR, 'values-cu.yaml')
SINGLE_DU_VALUES_FILE_PATH = os.path.join(SINGLE_DU_BASE_DIR, 'values-du.yaml')
SINGLE_UE_VALUES_FILE_PATH = os.path.join(SINGLE_UE_BASE_DIR, 'values-ue.yaml')

MULTI_GNB_CU_VALUES_FILE_PATH = os.path.join(MULTI_GNB_CU_BASE_DIR, 'values-cu.yaml')
MULTI_GNB_DU1_VALUES_FILE_PATH = os.path.join(MULTI_GNB_DU1_BASE_DIR, 'values-du.yaml')
MULTI_GNB_DU2_VALUES_FILE_PATH = os.path.join(MULTI_GNB_DU2_BASE_DIR, 'values-du.yaml')
MULTI_GNB_UE_VALUES_FILE_PATH = os.path.join(MULTI_GNB_UE_BASE_DIR, 'values-ue.yaml')

MULTI_UE_CU_VALUES_FILE_PATH = os.path.join(MULTI_UE_CU_BASE_DIR, 'values-cu.yaml')
MULTI_UE_DU_VALUES_FILE_PATH = os.path.join(MULTI_UE_DU_BASE_DIR, 'values-du.yaml')
MULTI_UE_UE1_VALUES_FILE_PATH = os.path.join(MULTI_UE_UE1_BASE_DIR, 'values-ue.yaml')
MULTI_UE_UE2_VALUES_FILE_PATH = os.path.join(MULTI_UE_UE2_BASE_DIR, 'values-ue.yaml')

@api_view(['GET'])
def endpoints(request):
    routes = [
        '/api/v1/oai/single-cu-config',
        '/api/v1/oai/single-du-config',
        '/api/v1/oai/single-ue-config',
        '/api/v1/oai/multignb-cu-config',
        '/api/v1/oai/multignb-du1-config',
        '/api/v1/oai/multignb-du2-config',
        '/api/v1/oai/multignb-ue-config',
        '/api/v1/oai/multiue-cu-config',
        '/api/v1/oai/multiue-du-config',
        '/api/v1/oai/multiue-ue1-config',
        '/api/v1/oai/multiue-ue2-config',
        '/api/v1/oai/create-all-5g',
    ]
    return Response(routes)


###CREATE ALL 5G COMPONENT NEEDED BY THE USER###
def CreateAll5G(request, namespace):
    try:        
        user_profile = UserProfile.objects.get(user=request.user)
        user_level = user_profile.level

        if user_level == 1:
            #SINGLE - CU
            subprocess.run([
                "helm", "install", "single-cu", "--values", "values-cu.yaml",
                ".", "--namespace", namespace
            ], cwd=SINGLE_CU_BASE_DIR)

            #SINGLE - DU
            subprocess.run([
                "helm", "install", "single-du", "--values", "values-du.yaml",
                ".", "--namespace", namespace
            ], cwd=SINGLE_DU_BASE_DIR)

            #SINGLE - UE
            subprocess.run([
                "helm", "install", "single-ue", "--values", "values-ue.yaml",
                ".", "--namespace", namespace
            ], cwd=SINGLE_UE_BASE_DIR)

        elif user_level == 2:
            #MULTI-GNB - CU
            subprocess.run([
                "helm", "install", "multignb-cu", "--values", "values-cu.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_GNB_CU_BASE_DIR)

            #MULTI-GNB - DU1
            subprocess.run([
                "helm", "install", "multignb-du1", "--values", "values-du.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_GNB_DU1_BASE_DIR)

            #MULTI-GNB - DU2
            subprocess.run([
                "helm", "install", "multignb-du2", "--values", "values-du.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_GNB_DU2_BASE_DIR)

            #MULTI-GNB - UE
            subprocess.run([
                "helm", "install", "multignb-ue", "--values", "values-ue.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_GNB_UE_BASE_DIR)

        elif user_level == 3:
            #MULTI-UE - CU
            subprocess.run([
                "helm", "install", "multiue-cu", "--values", "values-cu.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_UE_CU_BASE_DIR)

            #MULTI-UE - DU
            subprocess.run([
                "helm", "install", "multiue-du", "--values", "values-du.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_UE_DU_BASE_DIR)

            #MULTI-UE - UE1
            subprocess.run([
                "helm", "install", "multiue-ue1", "--values", "values-ue.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_UE_UE1_BASE_DIR)

            #MULTI-UE - UE2
            subprocess.run([
                "helm", "install", "multiue-ue2", "--values", "values-ue.yaml",
                ".", "--namespace", namespace
            ], cwd=MULTI_UE_UE2_BASE_DIR)

        return "Success"

    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocesses
        return f"An error occurred: {e}"


###DELETE ALL 5G COMPONENT ALONGSIDE USER ACCOUNT DELETION###
def DeleteAll5G(request, namespace):
    try:
        #SINGLE - CU
        subprocess.run([
            "helm", "delete", "single-cu", "--namespace", namespace
        ])

        #SINGLE - DU
        subprocess.run([
            "helm", "delete", "single-du", "--namespace", namespace
        ])

        #SINGLE - UE
        subprocess.run([
            "helm", "delete", "single-ue", "--namespace", namespace
        ])

        #MULTI-GNB - CU
        subprocess.run([
            "helm", "delete", "multignb-cu", "--namespace", namespace
        ])

        #MULTI-GNB - DU1
        subprocess.run([
            "helm", "delete", "multignb-du1", "--namespace", namespace
        ])

        #MULTI-GNB - DU2
        subprocess.run([
            "helm", "delete", "multignb-du2", "--namespace", namespace
        ])

        #MULTI-GNB - UE
        subprocess.run([
            "helm", "delete", "multignb-ue", "--namespace", namespace
        ])

        #MULTI-UE - CU
        subprocess.run([
            "helm", "delete", "multiue-cu", "--namespace", namespace
        ])

        #MULTI-UE - DU
        subprocess.run([
            "helm", "delete", "multiue-du", "--namespace", namespace
        ])

        #MULTI-UE - UE1
        subprocess.run([
            "helm", "delete", "multiue-ue1", "--namespace", namespace
        ])

        #MULTI-UE - UE2
        subprocess.run([
            "helm", "delete", "multiue-ue2", "--namespace", namespace
        ])

        # Delete the role and rolebinding
        role_name = f"{namespace}-role"
        role_binding_name = f"{namespace}-rolebinding"
        subprocess.run(["kubectl", "delete", "role", role_name, "--namespace", namespace])
        subprocess.run(["kubectl", "delete", "rolebinding", role_binding_name, "--namespace", namespace])

        # Delete the namespace
        subprocess.run(["kubectl", "delete", "namespace", namespace])

        return HttpResponse('Kubernetes resources successfully deleted')

    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocesses
        return HttpResponse(f"An error occurred: {e}")


###SINGLE - CU###
def ConfigSingleCU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(SINGLE_CU_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(SINGLE_CU_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "single-cu", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "single-cu", "--values", "values-cu.yaml",
            ".", "--namespace", namespace
        ], cwd=SINGLE_CU_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_single_cu.html')

###SINGLE - DU###
def ConfigSingleDU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(SINGLE_DU_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(SINGLE_DU_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "single-du", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "single-du", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=SINGLE_DU_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_single_du.html')

###SINGLE - UE###
def ConfigSingleUE(request):
    if request.method == 'POST':
        # Get the form data
        multus_int = request.POST.get('multus_int')
        multus_netmask = request.POST.get('multus_netmask')
        multus_gateway = request.POST.get('multus_gateway')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(SINGLE_UE_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['ipadd'] = multus_int
        values_data['multus']['netmask'] = multus_netmask
        values_data['multus']['defaultGateway'] = multus_gateway

        
        # Write the updated data back to the YAML file
        with open(SINGLE_UE_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "single-ue", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "single-ue", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=SINGLE_UE_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_single_ue.html')


###MULTIGNB - CU###
def ConfigMultignbCU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_GNB_CU_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(MULTI_GNB_CU_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multignb-cu", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multignb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_CU_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multignb_cu.html')

###MULTIGNB - DU1###
def ConfigMultignbDU1(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_GNB_DU1_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(MULTI_GNB_DU1_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multignb-du1", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multignb-du1", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_DU1_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multignb_du1.html')

###MULTIGNB - DU2###
def ConfigMultignbDU2(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_GNB_DU2_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(MULTI_GNB_DU2_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multignb-du2", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multignb-du2", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_DU2_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multignb_du2.html')

###MULTIGNB - UE###
def ConfigMultignbUE(request):
    if request.method == 'POST':
        # Get the form data
        multus_int = request.POST.get('multus_int')
        multus_netmask = request.POST.get('multus_netmask')
        multus_gateway = request.POST.get('multus_gateway')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_GNB_UE_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['ipadd'] = multus_int
        values_data['multus']['netmask'] = multus_netmask
        values_data['multus']['defaultGateway'] = multus_gateway

        
        # Write the updated data back to the YAML file
        with open(MULTI_GNB_UE_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multignb-ue", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multignb-ue", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_UE_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multignb_ue.html')


###MULTIUE - CU###
def ConfigMultiueCU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_UE_CU_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(MULTI_UE_CU_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multiue-cu", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multiue-cu", "--values", "values-cu.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_CU_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multiue_cu.html')

###MULTIUE - DU###
def ConfigMultiueDU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_UE_DU_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(MULTI_UE_DU_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multiue-du", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multiue-du", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_DU_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multiue_du.html')

###MULTIUE - UE1###
def ConfigMultiueUE1(request):
    if request.method == 'POST':
        # Get the form data
        multus_int = request.POST.get('multus_int')
        multus_netmask = request.POST.get('multus_netmask')
        multus_gateway = request.POST.get('multus_gateway')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_UE_UE1_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['ipadd'] = multus_int
        values_data['multus']['netmask'] = multus_netmask
        values_data['multus']['defaultGateway'] = multus_gateway

        
        # Write the updated data back to the YAML file
        with open(MULTI_UE_UE1_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multiue-ue1", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multiue-ue1", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_UE1_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multiue_ue1.html')

###MULTIUE - UE2###
def ConfigMultiueUE2(request):
    if request.method == 'POST':
        # Get the form data
        multus_int = request.POST.get('multus_int')
        multus_netmask = request.POST.get('multus_netmask')
        multus_gateway = request.POST.get('multus_gateway')
        
        # Derive the namespace from the current user's username
        namespace = f"{request.user.username}-namespace"

        # Load the existing YAML file
        with open(MULTI_UE_UE2_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['ipadd'] = multus_int
        values_data['multus']['netmask'] = multus_netmask
        values_data['multus']['defaultGateway'] = multus_gateway

        
        # Write the updated data back to the YAML file
        with open(MULTI_UE_UE2_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "multiue-ue2", "--namespace", namespace
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "multiue-ue2", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_UE2_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multiue_ue2.html')


###SINGLE CU - START###
def StartSingleCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "single-cu", "--values", "values-cu.yaml",
            ".", "--namespace", namespace
        ], cwd=SINGLE_CU_BASE_DIR)
        return HttpResponse("CU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE DU - START###
def StartSingleDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "single-du", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=SINGLE_DU_BASE_DIR)
        return HttpResponse("DU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE UE - START###
def StartSingleUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "single-ue", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=SINGLE_UE_BASE_DIR)
        return HttpResponse("UE started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB CU - START###
def StartMultignbCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multignb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_CU_BASE_DIR)
        return HttpResponse("CU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU1 - START###
def StartMultignbDU1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multignb-du1", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_DU1_BASE_DIR)
        return HttpResponse("DU1 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU2 - START###
def StartMultignbDU2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multignb-du2", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_DU2_BASE_DIR)
        return HttpResponse("DU2 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB UE - START###
def StartMultignbUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multignb-ue", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_GNB_UE_BASE_DIR)
        return HttpResponse("UE started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE CU - START###
def StartMultiueCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multiue-cu", "--values", "values-cu.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_CU_BASE_DIR)
        return HttpResponse("CU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE DU - START###
def StartMultiueDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multiue-du", "--values", "values-du.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_DU_BASE_DIR)
        return HttpResponse("DU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE1 - START###
def StartMultiueUE1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multiue-ue1", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_UE1_BASE_DIR)
        return HttpResponse("UE1 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE2 - START###
def StartMultiueUE2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "install", "multiue-ue2", "--values", "values-ue.yaml",
            ".", "--namespace", namespace
        ], cwd=MULTI_UE_UE2_BASE_DIR)
        return HttpResponse("UE2 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")


###SINGLE CU - STOP###
def StopSingleCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "single-cu", "--namespace", namespace
        ])
        return HttpResponse("CU stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE DU - STOP###
def StopSingleDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "single-du", "--namespace", namespace
        ])
        return HttpResponse("DU stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE UE - STOP###
def StopSingleUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "nr-ue", "--namespace", namespace
        ])
        return HttpResponse("UE stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB CU - STOP###
def StopMultignbCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "gnb-cu", "--namespace", namespace
        ])
        return HttpResponse("CU stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU1 - STOP###
def StopMultignbDU1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "gnb-du1", "--namespace", namespace
        ])
        return HttpResponse("DU1 stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU2 - STOP###
def StopMultignbDU2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "gnb-du2", "--namespace", namespace
        ])
        return HttpResponse("DU2 stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB UE - STOP###
def StopMultignbUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "nr-ue", "--namespace", namespace
        ])
        return HttpResponse("UE stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE CU - STOP###
def StopMultiueCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "gnb-cu", "--namespace", namespace
        ])
        return HttpResponse("CU stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE DU - STOP###
def StopMultiueDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "gnb-du", "--namespace", namespace
        ])
        return HttpResponse("DU stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE1 - STOP###
def StopMultiueUE1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "nr-ue1", "--namespace", namespace
        ])
        return HttpResponse("UE1 stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE2 - STOP###
def StopMultiueUE2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "helm", "delete", "nr-ue2", "--namespace", namespace
        ])
        return HttpResponse("UE2 stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

