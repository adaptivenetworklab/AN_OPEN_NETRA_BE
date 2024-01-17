from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import subprocess
import yaml
import os


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

###SINGLE - CU###
def ConfigSingleCU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
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
            "kubectl", "delete", "deployments", "oai-cu", "--namespace", "oai-gnb-ue"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "gnb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", "oai-gnb-ue"
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
            "kubectl", "delete", "deployments", "oai-du", "--namespace", "oai-gnb-ue"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "gnb-du", "--values", "values-du.yaml",
            ".", "--namespace", "oai-gnb-ue"
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
            "kubectl", "delete", "deployments", "oai-nr-ue", "--namespace", "oai-gnb-ue"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "nr-ue", "--values", "values-ue.yaml",
            ".", "--namespace", "oai-gnb-ue"
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
            "kubectl", "delete", "deployments", "oai-cu", "--namespace", "oai-multi-gnb"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "gnb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", "oai-multi-gnb"
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
            "kubectl", "delete", "deployments", "oai-du1", "--namespace", "oai-multi-gnb"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "gnb-du1", "--values", "values-du.yaml",
            ".", "--namespace", "oai-multi-gnb"
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
            "kubectl", "delete", "deployments", "oai-du2", "--namespace", "oai-multi-gnb"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "gnb-du2", "--values", "values-du.yaml",
            ".", "--namespace", "oai-multi-gnb"
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
            "kubectl", "delete", "deployments", "oai-nr-ue", "--namespace", "oai-multi-gnb"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "nr-ue", "--values", "values-ue.yaml",
            ".", "--namespace", "oai-multi-gnb"
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
            "kubectl", "delete", "deployments", "oai-cu", "--namespace", "oai-multi-ue"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "gnb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", "oai-multi-ue"
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
            "kubectl", "delete", "deployments", "oai-du", "--namespace", "oai-multi-ue"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "gnb-du", "--values", "values-du.yaml",
            ".", "--namespace", "oai-multi-ue"
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
            "kubectl", "delete", "deployments", "oai-nr-ue1", "--namespace", "oai-multi-ue"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "nr-ue1", "--values", "values-ue.yaml",
            ".", "--namespace", "oai-multi-ue"
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
            "kubectl", "delete", "deployments", "oai-nr-ue2", "--namespace", "oai-multi-ue"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "nr-ue2", "--values", "values-ue.yaml",
            ".", "--namespace", "oai-multi-ue"
        ], cwd=MULTI_UE_UE2_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'config_multiue_ue2.html')


###CREATE ALL 5G COMPONENT NEEDED BY THE USER###
def CreateAll5G(request):
    try:
        #SINGLE - CU
        subprocess.run([
            "helm", "install", "gnb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", "test1"
        ], cwd=SINGLE_CU_BASE_DIR)

        #SINGLE - DU
        subprocess.run([
            "helm", "install", "gnb-du", "--values", "values-du.yaml",
            ".", "--namespace", "test1"
        ], cwd=SINGLE_DU_BASE_DIR)

        #SINGLE - UE
        subprocess.run([
            "helm", "install", "nr-ue", "--values", "values-ue.yaml",
            ".", "--namespace", "test1"
        ], cwd=SINGLE_UE_BASE_DIR)

        #MULTI-GNB - CU
        subprocess.run([
            "helm", "install", "gnb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", "test2"
        ], cwd=MULTI_GNB_CU_BASE_DIR)

        #MULTI-GNB - DU1
        subprocess.run([
            "helm", "install", "gnb-du1", "--values", "values-du.yaml",
            ".", "--namespace", "test2"
        ], cwd=MULTI_GNB_DU1_BASE_DIR)

        #MULTI-GNB - DU2
        subprocess.run([
            "helm", "install", "gnb-du2", "--values", "values-du.yaml",
            ".", "--namespace", "test2"
        ], cwd=MULTI_GNB_DU2_BASE_DIR)

        #MULTI-GNB - UE
        subprocess.run([
            "helm", "install", "nr-ue", "--values", "values-ue.yaml",
            ".", "--namespace", "test2"
        ], cwd=MULTI_GNB_UE_BASE_DIR)

        #MULTI-UE - CU
        subprocess.run([
            "helm", "install", "gnb-cu", "--values", "values-cu.yaml",
            ".", "--namespace", "test3"
        ], cwd=MULTI_UE_CU_BASE_DIR)

        #MULTI-UE - DU
        subprocess.run([
            "helm", "install", "gnb-du", "--values", "values-du.yaml",
            ".", "--namespace", "test3"
        ], cwd=MULTI_UE_DU_BASE_DIR)

        #MULTI-UE - UE1
        subprocess.run([
            "helm", "install", "nr-ue1", "--values", "values-ue.yaml",
            ".", "--namespace", "test3"
        ], cwd=MULTI_UE_UE1_BASE_DIR)

        #MULTI-UE - UE2
        subprocess.run([
            "helm", "install", "nr-ue2", "--values", "values-ue.yaml",
            ".", "--namespace", "test3"
        ], cwd=MULTI_UE_UE2_BASE_DIR)

        return HttpResponse('User Successfully Added')

    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocesses
        return HttpResponse(f"An error occurred: {e}")
