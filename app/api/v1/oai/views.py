from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import subprocess
import yaml
import os
from app.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


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
def ValuesSingleCU(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "single-cu", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # It seems like the structure might differ. Make sure to access the correct path.
        # Extract specific values assuming 'values' is the top-level key as per your example.
        specific_values = {
            'cuName': values_json.get('config', {}).get('cuName', ''),
            'f1IfName': values_json.get('config', {}).get('f1IfName', ''),
            # For multus values, ensure you're accessing the multus configuration correctly
            'f1InterfaceIPadd': values_json.get('multus', {}).get('f1Interface', {}).get('IPadd', ''),
            'f1cuPort': values_json.get('config', {}).get('f1cuPort', ''),
            'f1duPort': values_json.get('config', {}).get('f1duPort', ''),
            'n2IfName': values_json.get('config', {}).get('n2IfName', ''),
            'n2InterfaceIPadd': values_json.get('multus', {}).get('n2Interface', {}).get('IPadd', ''),
            'n3IfName': values_json.get('config', {}).get('n3IfName', ''),
            'n3InterfaceIPadd': values_json.get('multus', {}).get('n3Interface', {}).get('IPadd', ''),
            'mcc': values_json.get('config', {}).get('mcc', ''),
            'mnc': values_json.get('config', {}).get('mnc', ''),
            'tac': values_json.get('config', {}).get('tac', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'amfhost': values_json.get('config', {}).get('amfhost', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###SINGLE - DU###
def ValuesSingleDU(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "single-du", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'duName': values_json.get('config', {}).get('duName', ''),
            'f1IfName': values_json.get('config', {}).get('f1IfName', ''),
            'f1InterfaceIPadd': values_json.get('multus', {}).get('f1Interface', {}).get('IPadd', ''),
            'f1cuPort': values_json.get('config', {}).get('f1cuPort', ''),
            'f1duPort': values_json.get('config', {}).get('f1duPort', ''),
            'mcc': values_json.get('config', {}).get('mcc', ''),
            'mnc': values_json.get('config', {}).get('mnc', ''),
            'tac': values_json.get('config', {}).get('tac', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'usrp': values_json.get('config', {}).get('usrp', ''),
            'cuHost': values_json.get('config', {}).get('cuHost', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###SINGLE - UE###
def ValuesSingleUE(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "single-ue", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'multusIPadd': values_json.get('multus', {}).get('ipadd', ''),
            'rfSimServer': values_json.get('config', {}).get('rfSimServer', ''),
            'fullImsi': values_json.get('config', {}).get('fullImsi', ''),
            'fullKey': values_json.get('config', {}).get('fullKey', ''),
            'opc': values_json.get('config', {}).get('opc', ''),
            'dnn': values_json.get('config', {}).get('dnn', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'sd': values_json.get('config', {}).get('sd', ''),
            'usrp': values_json.get('config', {}).get('usrp', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)


###MULTIGNB - CU###
def ValuesMultignbCU(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "single-cu", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # It seems like the structure might differ. Make sure to access the correct path.
        # Extract specific values assuming 'values' is the top-level key as per your example.
        specific_values = {
            'cuName': values_json.get('config', {}).get('cuName', ''),
            'f1IfName': values_json.get('config', {}).get('f1IfName', ''),
            # For multus values, ensure you're accessing the multus configuration correctly
            'f1InterfaceIPadd': values_json.get('multus', {}).get('f1Interface', {}).get('IPadd', ''),
            'f1cuPort': values_json.get('config', {}).get('f1cuPort', ''),
            'f1duPort': values_json.get('config', {}).get('f1duPort', ''),
            'n2IfName': values_json.get('config', {}).get('n2IfName', ''),
            'n2InterfaceIPadd': values_json.get('multus', {}).get('n2Interface', {}).get('IPadd', ''),
            'n3IfName': values_json.get('config', {}).get('n3IfName', ''),
            'n3InterfaceIPadd': values_json.get('multus', {}).get('n3Interface', {}).get('IPadd', ''),
            'mcc': values_json.get('config', {}).get('mcc', ''),
            'mnc': values_json.get('config', {}).get('mnc', ''),
            'tac': values_json.get('config', {}).get('tac', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'amfhost': values_json.get('config', {}).get('amfhost', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###GMULTIGNB - DU1###
def ValuesMultignbDU1(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "multignb-du1", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'duName': values_json.get('config', {}).get('duName', ''),
            'f1IfName': values_json.get('config', {}).get('f1IfName', ''),
            'f1InterfaceIPadd': values_json.get('multus', {}).get('f1Interface', {}).get('IPadd', ''),
            'f1cuPort': values_json.get('config', {}).get('f1cuPort', ''),
            'f1duPort': values_json.get('config', {}).get('f1duPort', ''),
            'ruInterfaceIPadd': values_json.get('multus', {}).get('ruInterface', {}).get('IPadd', ''),
            'mcc': values_json.get('config', {}).get('mcc', ''),
            'mnc': values_json.get('config', {}).get('mnc', ''),
            'tac': values_json.get('config', {}).get('tac', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'usrp': values_json.get('config', {}).get('usrp', ''),
            'cuHost': values_json.get('config', {}).get('cuHost', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###MULTIGNB - DU2###
def ValuesMultignbDU2(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "multignb-du2", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'duName': values_json.get('config', {}).get('duName', ''),
            'f1IfName': values_json.get('config', {}).get('f1IfName', ''),
            'f1InterfaceIPadd': values_json.get('multus', {}).get('f1Interface', {}).get('IPadd', ''),
            'f1cuPort': values_json.get('config', {}).get('f1cuPort', ''),
            'f1duPort': values_json.get('config', {}).get('f1duPort', ''),
            'ruInterfaceIPadd': values_json.get('multus', {}).get('ruInterface', {}).get('IPadd', ''),
            'mcc': values_json.get('config', {}).get('mcc', ''),
            'mnc': values_json.get('config', {}).get('mnc', ''),
            'tac': values_json.get('config', {}).get('tac', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'usrp': values_json.get('config', {}).get('usrp', ''),
            'cuHost': values_json.get('config', {}).get('cuHost', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###MULTIGNB - UE###
def ValuesMultignbUE(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "multignb-ue", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'multusIPadd': values_json.get('multus', {}).get('ipadd', ''),
            'rfSimServer': values_json.get('config', {}).get('rfSimServer', ''),
            'fullImsi': values_json.get('config', {}).get('fullImsi', ''),
            'fullKey': values_json.get('config', {}).get('fullKey', ''),
            'opc': values_json.get('config', {}).get('opc', ''),
            'dnn': values_json.get('config', {}).get('dnn', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'sd': values_json.get('config', {}).get('sd', ''),
            'usrp': values_json.get('config', {}).get('usrp', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)


###MULTIUE - CU###
def ValuesMultiueCU(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "single-cu", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # It seems like the structure might differ. Make sure to access the correct path.
        # Extract specific values assuming 'values' is the top-level key as per your example.
        specific_values = {
            'cuName': values_json.get('config', {}).get('cuName', ''),
            'f1IfName': values_json.get('config', {}).get('f1IfName', ''),
            # For multus values, ensure you're accessing the multus configuration correctly
            'f1InterfaceIPadd': values_json.get('multus', {}).get('f1Interface', {}).get('IPadd', ''),
            'f1cuPort': values_json.get('config', {}).get('f1cuPort', ''),
            'f1duPort': values_json.get('config', {}).get('f1duPort', ''),
            'n2IfName': values_json.get('config', {}).get('n2IfName', ''),
            'n2InterfaceIPadd': values_json.get('multus', {}).get('n2Interface', {}).get('IPadd', ''),
            'n3IfName': values_json.get('config', {}).get('n3IfName', ''),
            'n3InterfaceIPadd': values_json.get('multus', {}).get('n3Interface', {}).get('IPadd', ''),
            'mcc': values_json.get('config', {}).get('mcc', ''),
            'mnc': values_json.get('config', {}).get('mnc', ''),
            'tac': values_json.get('config', {}).get('tac', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'amfhost': values_json.get('config', {}).get('amfhost', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###MULTIUE - DU###
def ValuesMultiueDU(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "multiue-du", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'duName': values_json.get('config', {}).get('duName', ''),
            'f1IfName': values_json.get('config', {}).get('f1IfName', ''),
            'f1InterfaceIPadd': values_json.get('multus', {}).get('f1Interface', {}).get('IPadd', ''),
            'f1cuPort': values_json.get('config', {}).get('f1cuPort', ''),
            'f1duPort': values_json.get('config', {}).get('f1duPort', ''),
            'ruInterfaceIPadd': values_json.get('multus', {}).get('ruInterface', {}).get('IPadd', ''),
            'mcc': values_json.get('config', {}).get('mcc', ''),
            'mnc': values_json.get('config', {}).get('mnc', ''),
            'tac': values_json.get('config', {}).get('tac', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'usrp': values_json.get('config', {}).get('usrp', ''),
            'cuHost': values_json.get('config', {}).get('cuHost', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###MULTIUE - UE1###
def ValuesMultiueUE1(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "multiue-ue1", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'multusIPadd': values_json.get('multus', {}).get('ipadd', ''),
            'rfSimServer': values_json.get('config', {}).get('rfSimServer', ''),
            'fullImsi': values_json.get('config', {}).get('fullImsi', ''),
            'fullKey': values_json.get('config', {}).get('fullKey', ''),
            'opc': values_json.get('config', {}).get('opc', ''),
            'dnn': values_json.get('config', {}).get('dnn', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'sd': values_json.get('config', {}).get('sd', ''),
            'usrp': values_json.get('config', {}).get('usrp', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)

###MULTIUE - UE2###
def ValuesMultiueUE2(request):
    user_namespace = f"{request.user.username}-namespace"

    # Execute helm get values command
    command = ["helm", "get", "values", "multiue-ue2", "--namespace", user_namespace]
    try:
        helm_output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        values_yaml = helm_output.decode('utf-8')

        # Convert YAML to JSON
        values_json = yaml.safe_load(values_yaml)  # Assumes PyYAML or similar package is used

        # Extract specific values
        specific_values = {
            'multusIPadd': values_json.get('multus', {}).get('ipadd', ''),
            'rfSimServer': values_json.get('config', {}).get('rfSimServer', ''),
            'fullImsi': values_json.get('config', {}).get('fullImsi', ''),
            'fullKey': values_json.get('config', {}).get('fullKey', ''),
            'opc': values_json.get('config', {}).get('opc', ''),
            'dnn': values_json.get('config', {}).get('dnn', ''),
            'sst': values_json.get('config', {}).get('sst', ''),
            'sd': values_json.get('config', {}).get('sd', ''),
            'usrp': values_json.get('config', {}).get('usrp', '')
        }

        return JsonResponse({'values': specific_values})

    except subprocess.CalledProcessError as e:
        return JsonResponse({'error': 'Failed to retrieve Helm release values',
                             'details': e.output.decode('utf-8')}, status=500)

    except Exception as e:
        return JsonResponse({'error': 'An unexpected error occurred',
                             'details': str(e)}, status=500)


###SINGLE - CU###
def ConfigSingleCU(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "single-cu", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'cu_name' in request.POST and request.POST['cu_name']:
        current_values['config']['cuName'] = request.POST['cu_name']
    if 'f1_ifname' in request.POST and request.POST['f1_ifname']:
        current_values['config']['f1IfName'] = request.POST['f1_ifname']
    if 'f1_int' in request.POST and request.POST['f1_int']:
        current_values['multus']['f1Interface']['IPadd'] = request.POST['f1_int']
    if 'f1_cuport' in request.POST and request.POST['f1_cuport']:
        current_values['config']['f1cuPort'] = request.POST['f1_cuport']
    if 'f1_duport' in request.POST and request.POST['f1_duport']:
        current_values['config']['f1duPort'] = request.POST['f1_duport']
    if 'n2_ifname' in request.POST and request.POST['n2_ifname']:
        current_values['config']['n2IfName'] = request.POST['n2_ifname']
    if 'n2_int' in request.POST and request.POST['n2_int']:
        current_values['multus']['n2Interface']['IPadd'] = request.POST['n2_int']
    if 'n3_ifname' in request.POST and request.POST['n3_ifname']:
        current_values['config']['n3IfName'] = request.POST['n3_ifname']
    if 'n3_int' in request.POST and request.POST['n3_int']:
        current_values['multus']['n3Interface']['IPadd'] = request.POST['n3_int']
    if 'mcc' in request.POST and request.POST['mcc']:
        current_values['config']['mcc'] = request.POST['mcc']
    if 'mnc' in request.POST and request.POST['mnc']:
        current_values['config']['mnc'] = request.POST['mnc']
    if 'tac' in request.POST and request.POST['tac']:
        current_values['config']['tac'] = request.POST['tac']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'amf_host' in request.POST and request.POST['amf_host']:
        current_values['config']['amfhost'] = request.POST['amf_host']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "single-cu", SINGLE_CU_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###SINGLE - DU###
def ConfigSingleDU(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "single-du", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'du_name' in request.POST and request.POST['du_name']:
        current_values['config']['duName'] = request.POST['du_name']
    if 'f1_ifname' in request.POST and request.POST['f1_ifname']:
        current_values['config']['f1IfName'] = request.POST['f1_ifname']
    if 'f1_int' in request.POST and request.POST['f1_int']:
        current_values['multus']['f1Interface']['IPadd'] = request.POST['f1_int']
    if 'f1_cuport' in request.POST and request.POST['f1_cuport']:
        current_values['config']['f1cuPort'] = request.POST['f1_cuport']
    if 'f1_duport' in request.POST and request.POST['f1_duport']:
        current_values['config']['f1duPort'] = request.POST['f1_duport']
    if 'mcc' in request.POST and request.POST['mcc']:
        current_values['config']['mcc'] = request.POST['mcc']
    if 'mnc' in request.POST and request.POST['mnc']:
        current_values['config']['mnc'] = request.POST['mnc']
    if 'tac' in request.POST and request.POST['tac']:
        current_values['config']['tac'] = request.POST['tac']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    if 'cu_host' in request.POST and request.POST['cu_host']:
        current_values['config']['cuHost'] = request.POST['cu_host']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "single-du", SINGLE_DU_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###SINGLE - UE###
def ConfigSingleUE(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "single-ue", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'multus_ipadd' in request.POST and request.POST['multus_ipadd']:
        current_values['multus']['ipadd'] = request.POST['multus_ipadd']
    if 'rfsimserver' in request.POST and request.POST['rfsimserver']:
        current_values['config']['rfSimServer'] = request.POST['rfsimserver']
    if 'fullimsi' in request.POST and request.POST['fullimsi']:
        current_values['config']['fullImsi'] = request.POST['fullimsi']
    if 'fullkey' in request.POST and request.POST['fullkey']:
        current_values['config']['fullKey'] = request.POST['fullkey']
    if 'opc' in request.POST and request.POST['opc']:
        current_values['config']['opc'] = request.POST['opc']
    if 'dnn' in request.POST and request.POST['dnn']:
        current_values['config']['dnn'] = request.POST['dnn']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'sd' in request.POST and request.POST['sd']:
        current_values['config']['sd'] = request.POST['sd']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "single-ue", SINGLE_UE_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")


###MULTIGNB - CU###
def ConfigMultignbCU(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multignb-cu", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'cu_name' in request.POST and request.POST['cu_name']:
        current_values['config']['cuName'] = request.POST['cu_name']
    if 'f1_ifname' in request.POST and request.POST['f1_ifname']:
        current_values['config']['f1IfName'] = request.POST['f1_ifname']
    if 'f1_int' in request.POST and request.POST['f1_int']:
        current_values['multus']['f1Interface']['IPadd'] = request.POST['f1_int']
    if 'f1_cuport' in request.POST and request.POST['f1_cuport']:
        current_values['config']['f1cuPort'] = request.POST['f1_cuport']
    if 'f1_duport' in request.POST and request.POST['f1_duport']:
        current_values['config']['f1duPort'] = request.POST['f1_duport']
    if 'n2_ifname' in request.POST and request.POST['n2_ifname']:
        current_values['config']['n2IfName'] = request.POST['n2_ifname']
    if 'n2_int' in request.POST and request.POST['n2_int']:
        current_values['multus']['n2Interface']['IPadd'] = request.POST['n2_int']
    if 'n3_ifname' in request.POST and request.POST['n3_ifname']:
        current_values['config']['n3IfName'] = request.POST['n3_ifname']
    if 'n3_int' in request.POST and request.POST['n3_int']:
        current_values['multus']['n3Interface']['IPadd'] = request.POST['n3_int']
    if 'mcc' in request.POST and request.POST['mcc']:
        current_values['config']['mcc'] = request.POST['mcc']
    if 'mnc' in request.POST and request.POST['mnc']:
        current_values['config']['mnc'] = request.POST['mnc']
    if 'tac' in request.POST and request.POST['tac']:
        current_values['config']['tac'] = request.POST['tac']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'amf_host' in request.POST and request.POST['amf_host']:
        current_values['config']['amfhost'] = request.POST['amf_host']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multignb-cu", MULTIGNB_CU_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###MULTIGNB - DU1###
def ConfigMultignbDU1(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multignb-du1", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'du_name' in request.POST and request.POST['du_name']:
        current_values['config']['duName'] = request.POST['du_name']
    if 'f1_ifname' in request.POST and request.POST['f1_ifname']:
        current_values['config']['f1IfName'] = request.POST['f1_ifname']
    if 'f1_int' in request.POST and request.POST['f1_int']:
        current_values['multus']['f1Interface']['IPadd'] = request.POST['f1_int']
    if 'f1_cuport' in request.POST and request.POST['f1_cuport']:
        current_values['config']['f1cuPort'] = request.POST['f1_cuport']
    if 'f1_duport' in request.POST and request.POST['f1_duport']:
        current_values['config']['f1duPort'] = request.POST['f1_duport']
    if 'mcc' in request.POST and request.POST['mcc']:
        current_values['config']['mcc'] = request.POST['mcc']
    if 'mnc' in request.POST and request.POST['mnc']:
        current_values['config']['mnc'] = request.POST['mnc']
    if 'tac' in request.POST and request.POST['tac']:
        current_values['config']['tac'] = request.POST['tac']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    if 'cu_host' in request.POST and request.POST['cu_host']:
        current_values['config']['cuHost'] = request.POST['cu_host']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multignb-du1", MULTIGNB_DU1_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###MULTIGNB - DU2###
def ConfigMultignbDU2(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multignb-du2", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'du_name' in request.POST and request.POST['du_name']:
        current_values['config']['duName'] = request.POST['du_name']
    if 'f1_ifname' in request.POST and request.POST['f1_ifname']:
        current_values['config']['f1IfName'] = request.POST['f1_ifname']
    if 'f1_int' in request.POST and request.POST['f1_int']:
        current_values['multus']['f1Interface']['IPadd'] = request.POST['f1_int']
    if 'f1_cuport' in request.POST and request.POST['f1_cuport']:
        current_values['config']['f1cuPort'] = request.POST['f1_cuport']
    if 'f1_duport' in request.POST and request.POST['f1_duport']:
        current_values['config']['f1duPort'] = request.POST['f1_duport']
    if 'mcc' in request.POST and request.POST['mcc']:
        current_values['config']['mcc'] = request.POST['mcc']
    if 'mnc' in request.POST and request.POST['mnc']:
        current_values['config']['mnc'] = request.POST['mnc']
    if 'tac' in request.POST and request.POST['tac']:
        current_values['config']['tac'] = request.POST['tac']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    if 'cu_host' in request.POST and request.POST['cu_host']:
        current_values['config']['cuHost'] = request.POST['cu_host']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multignb-du2", MULTIGNB_DU2_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###MULTIGNB - UE###
def ConfigMultignbUE(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multignb-ue", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'multus_ipadd' in request.POST and request.POST['multus_ipadd']:
        current_values['multus']['ipadd'] = request.POST['multus_ipadd']
    if 'rfsimserver' in request.POST and request.POST['rfsimserver']:
        current_values['config']['rfSimServer'] = request.POST['rfsimserver']
    if 'fullimsi' in request.POST and request.POST['fullimsi']:
        current_values['config']['fullImsi'] = request.POST['fullimsi']
    if 'fullkey' in request.POST and request.POST['fullkey']:
        current_values['config']['fullKey'] = request.POST['fullkey']
    if 'opc' in request.POST and request.POST['opc']:
        current_values['config']['opc'] = request.POST['opc']
    if 'dnn' in request.POST and request.POST['dnn']:
        current_values['config']['dnn'] = request.POST['dnn']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'sd' in request.POST and request.POST['sd']:
        current_values['config']['sd'] = request.POST['sd']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multignb-ue", MULTIGNB_UE_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")



###MULTIUE - CU###
def ConfigMultiueCU(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multiue-cu", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'cu_name' in request.POST and request.POST['cu_name']:
        current_values['config']['cuName'] = request.POST['cu_name']
    if 'f1_ifname' in request.POST and request.POST['f1_ifname']:
        current_values['config']['f1IfName'] = request.POST['f1_ifname']
    if 'f1_int' in request.POST and request.POST['f1_int']:
        current_values['multus']['f1Interface']['IPadd'] = request.POST['f1_int']
    if 'f1_cuport' in request.POST and request.POST['f1_cuport']:
        current_values['config']['f1cuPort'] = request.POST['f1_cuport']
    if 'f1_duport' in request.POST and request.POST['f1_duport']:
        current_values['config']['f1duPort'] = request.POST['f1_duport']
    if 'n2_ifname' in request.POST and request.POST['n2_ifname']:
        current_values['config']['n2IfName'] = request.POST['n2_ifname']
    if 'n2_int' in request.POST and request.POST['n2_int']:
        current_values['multus']['n2Interface']['IPadd'] = request.POST['n2_int']
    if 'n3_ifname' in request.POST and request.POST['n3_ifname']:
        current_values['config']['n3IfName'] = request.POST['n3_ifname']
    if 'n3_int' in request.POST and request.POST['n3_int']:
        current_values['multus']['n3Interface']['IPadd'] = request.POST['n3_int']
    if 'mcc' in request.POST and request.POST['mcc']:
        current_values['config']['mcc'] = request.POST['mcc']
    if 'mnc' in request.POST and request.POST['mnc']:
        current_values['config']['mnc'] = request.POST['mnc']
    if 'tac' in request.POST and request.POST['tac']:
        current_values['config']['tac'] = request.POST['tac']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'amf_host' in request.POST and request.POST['amf_host']:
        current_values['config']['amfhost'] = request.POST['amf_host']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multiue-cu", MULTIUE_CU_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###MULTIUE - DU###
def ConfigMultiueDU(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multiue-du", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'du_name' in request.POST and request.POST['du_name']:
        current_values['config']['duName'] = request.POST['du_name']
    if 'f1_ifname' in request.POST and request.POST['f1_ifname']:
        current_values['config']['f1IfName'] = request.POST['f1_ifname']
    if 'f1_int' in request.POST and request.POST['f1_int']:
        current_values['multus']['f1Interface']['IPadd'] = request.POST['f1_int']
    if 'f1_cuport' in request.POST and request.POST['f1_cuport']:
        current_values['config']['f1cuPort'] = request.POST['f1_cuport']
    if 'f1_duport' in request.POST and request.POST['f1_duport']:
        current_values['config']['f1duPort'] = request.POST['f1_duport']
    if 'mcc' in request.POST and request.POST['mcc']:
        current_values['config']['mcc'] = request.POST['mcc']
    if 'mnc' in request.POST and request.POST['mnc']:
        current_values['config']['mnc'] = request.POST['mnc']
    if 'tac' in request.POST and request.POST['tac']:
        current_values['config']['tac'] = request.POST['tac']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    if 'cu_host' in request.POST and request.POST['cu_host']:
        current_values['config']['cuHost'] = request.POST['cu_host']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multiue-du", MULTIUE_DU_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###MULTIUE - UE1###
def ConfigMultiueUE1(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multiue-ue1", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'multus_ipadd' in request.POST and request.POST['multus_ipadd']:
        current_values['multus']['ipadd'] = request.POST['multus_ipadd']
    if 'rfsimserver' in request.POST and request.POST['rfsimserver']:
        current_values['config']['rfSimServer'] = request.POST['rfsimserver']
    if 'fullimsi' in request.POST and request.POST['fullimsi']:
        current_values['config']['fullImsi'] = request.POST['fullimsi']
    if 'fullkey' in request.POST and request.POST['fullkey']:
        current_values['config']['fullKey'] = request.POST['fullkey']
    if 'opc' in request.POST and request.POST['opc']:
        current_values['config']['opc'] = request.POST['opc']
    if 'dnn' in request.POST and request.POST['dnn']:
        current_values['config']['dnn'] = request.POST['dnn']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'sd' in request.POST and request.POST['sd']:
        current_values['config']['sd'] = request.POST['sd']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multiue-ue1", MULTIUE_UE1_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")

###MULTIUE - UE2###
def ConfigMultiueUE2(request):
    namespace = f"{request.user.username}-namespace"

    get_values_command = ["helm", "get", "values", "multiue-ue2", "--namespace", namespace, "--output", "yaml"]
    current_values_yaml = subprocess.check_output(get_values_command).decode("utf-8")
    current_values = yaml.safe_load(current_values_yaml)

    # Check if each field is provided in the form and update accordingly
    if 'multus_ipadd' in request.POST and request.POST['multus_ipadd']:
        current_values['multus']['ipadd'] = request.POST['multus_ipadd']
    if 'rfsimserver' in request.POST and request.POST['rfsimserver']:
        current_values['config']['rfSimServer'] = request.POST['rfsimserver']
    if 'fullimsi' in request.POST and request.POST['fullimsi']:
        current_values['config']['fullImsi'] = request.POST['fullimsi']
    if 'fullkey' in request.POST and request.POST['fullkey']:
        current_values['config']['fullKey'] = request.POST['fullkey']
    if 'opc' in request.POST and request.POST['opc']:
        current_values['config']['opc'] = request.POST['opc']
    if 'dnn' in request.POST and request.POST['dnn']:
        current_values['config']['dnn'] = request.POST['dnn']
    if 'sst' in request.POST and request.POST['sst']:
        current_values['config']['sst'] = request.POST['sst']
    if 'sd' in request.POST and request.POST['sd']:
        current_values['config']['sd'] = request.POST['sd']
    if 'usrp' in request.POST and request.POST['usrp']:
        current_values['config']['usrp'] = request.POST['usrp']
    
    # Convert updated values back to YAML string
    updated_values_yaml = yaml.dump(current_values)

    # Use a temporary file to pass the updated values to the helm upgrade command
    with open('updated_values.yaml', 'w') as temp_file:
        temp_file.write(updated_values_yaml)
    
    # Execute Helm upgrade command with the updated values
    upgrade_command = [
        "helm", "upgrade", "multiue-ue2", MULTIUE_UE2_BASE_DIR,
        "--namespace", namespace,
        "-f", 'updated_values.yaml'
    ]
    subprocess.run(upgrade_command)
    os.remove('updated_values.yaml')

    return HttpResponse("Configuration Updated Successfully")



###SINGLE CU - START###
def StartSingleCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "single-cu", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("CU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE DU - START###
def StartSingleDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "single-du", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE UE - START###
def StartSingleUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "single-ue", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB CU - START###
def StartMultignbCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-cu", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("CU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU1 - START###
def StartMultignbDU1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-du1", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU1 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU2 - START###
def StartMultignbDU2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-du2", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU2 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB UE - START###
def StartMultignbUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-ue", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE CU - START###
def StartMultiueCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-cu", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("CU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE DU - START###
def StartMultiueDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-du", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE1 - START###
def StartMultiueUE1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-ue1", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE1 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE2 - START###
def StartMultiueUE2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-ue2", "--replicas=1",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE2 started")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")


###SINGLE CU - STOP###
def StopSingleCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "single-cu", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("CU Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE DU - STOP###
def StopSingleDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "single-du", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###SINGLE UE - STOP###
def StopSingleUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "single-ue", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB CU - STOP###
def StopMultignbCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-cu", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("CU Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU1 - STOP###
def StopMultignbDU1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-du1", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU1 Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB DU2 - STOP###
def StopMultignbDU2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-du2", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU2 Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIGNB UE - STOP###
def StopMultignbUE(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multignb-ue", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE CU - STOP###
def StopMultiueCU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-cu", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("CU Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE DU - STOP###
def StopMultiueDU(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-du", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("DU Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE1 - STOP###
def StopMultiueUE1(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-ue1", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE1 Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")

###MULTIUE UE2 - STOP###
def StopMultiueUE2(request):
    try:
        username = request.user.username  # Get the currently logged-in user's username
        namespace = f"{username}-namespace"  # Construct the namespace based on the username

        subprocess.run([
            "kubectl", "scale", "deployment", "multiue-ue2", "--replicas=0",
            "--namespace=" + namespace
        ])
        return HttpResponse("UE2 Stopped")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"An error occurred: {e}")


