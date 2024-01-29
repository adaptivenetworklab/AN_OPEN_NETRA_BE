import subprocess

def check_helm_deployment_exists(deployment_name, namespace):
    try:
        result = subprocess.run(
            ["helm", "list", "--namespace", namespace, "-q"],
            capture_output=True, text=True
        )
        return deployment_name in result.stdout.split()
    except subprocess.CalledProcessError:
        return False