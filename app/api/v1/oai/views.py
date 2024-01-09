from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import subprocess
import yaml
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CU1_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-gnb-cu-1')  # Adjust 'subdirectory' as needed
CU2_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-gnb-cu-2')  # Adjust 'subdirectory' as needed
CU3_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-gnb-cu-3')  # Adjust 'subdirectory' as needed
DU1_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-gnb-du-1')  # Adjust 'subdirectory' as needed
DU2_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-gnb-du-2')  # Adjust 'subdirectory' as needed
DU3_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-gnb-du-3')  # Adjust 'subdirectory' as needed
UE1_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-nr-ue-1')  # Adjust 'subdirectory' as needed
UE2_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-nr-ue-2')  # Adjust 'subdirectory' as needed
UE3_BASE_DIR = os.path.join(BASE_DIR, 'oai/AN-OPEN-NETRA-VNF/oai-nr-ue-3')  # Adjust 'subdirectory' as needed
CU1_VALUES_FILE_PATH = os.path.join(CU1_BASE_DIR, 'values.yaml')
CU2_VALUES_FILE_PATH = os.path.join(CU2_BASE_DIR, 'values.yaml')
CU3_VALUES_FILE_PATH = os.path.join(CU3_BASE_DIR, 'values.yaml')
DU1_VALUES_FILE_PATH = os.path.join(DU1_BASE_DIR, 'values.yaml')
DU2_VALUES_FILE_PATH = os.path.join(DU2_BASE_DIR, 'values.yaml')
DU3_VALUES_FILE_PATH = os.path.join(DU3_BASE_DIR, 'values.yaml')
UE1_VALUES_FILE_PATH = os.path.join(UE1_BASE_DIR, 'values.yaml')
UE2_VALUES_FILE_PATH = os.path.join(UE2_BASE_DIR, 'values.yaml')
UE3_VALUES_FILE_PATH = os.path.join(UE3_BASE_DIR, 'values.yaml')


@api_view(['GET'])
def endpoints(request):
    routes = [
        '/api/v1/oai/create-cu',
        '/api/v1/oai/create-du',
        '/api/v1/oai/create-ue',
        '/api/v1/oai/update-values',
    ]
    return Response(routes)

def CreateCU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Load the existing YAML file
        with open(CU1_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(CU1_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        subprocess.run([
            "kubectl", "delete", "deployments", "oai-gnb-cu", "--namespace", "oai"
        ])

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "oai-gnb-cu", "--values", "values.yaml",
            ".", "--namespace", "oai"
        ], cwd=CU1_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")
    # For GET request, just show the form
    return render(request, 'create_cu.html')


def CreateDU(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Load the existing YAML file
        with open(DU1_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(DU1_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)
        
        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "oai-gnb-du", "--values", "values.yaml",
            ".", "--namespace", "oai"
        ], cwd=DU1_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")

    # For GET request, just show the form
    return render(request, 'create_du.html')

def CreateUE(request):
    if request.method == 'POST':
        # Get the form data
        multus_ip = request.POST.get('multus_ip')
        multus_netmask = request.POST.get('multus_netmask')
        
        # Load the existing YAML file
        with open(UE1_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['ipadd'] = multus_ip
        values_data['multus']['netmask'] = multus_netmask
        
        # Write the updated data back to the YAML file
        with open(UE1_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)

        # Execute Helm install command (Example: helm install my-release ./my-chart -f values.yaml)
        subprocess.run([
            "helm", "upgrade", "oai-nr-ue", "--values", "values.yaml",
            ".", "--namespace", "oai"
        ], cwd=UE1_BASE_DIR)
        
        return HttpResponse("Configuration Updated Successfully")

    # For GET request, just show the form
    return render(request, 'create_ue.html')

def update_values(request):
    if request.method == 'POST':
        # Get the form data
        multus_f1_int = request.POST.get('multus_f1_int')
        multus_f1_netmask = request.POST.get('multus_f1_netmask')
        
        # Load the existing YAML file
        with open(CU_VALUES_FILE_PATH, 'r') as file:
            values_data = yaml.safe_load(file)

        # # Update the YAML data
        values_data['multus']['f1Interface']['IPadd'] = multus_f1_int
        values_data['multus']['f1Interface']['Netmask'] = multus_f1_netmask
        
        # Write the updated data back to the YAML file
        with open(CU_VALUES_FILE_PATH, 'w') as file:
            yaml.dump(values_data, file)
        
        return HttpResponse("Configuration Updated Successfully")

    # For GET request, just show the form
    return render(request, 'update_values.html')