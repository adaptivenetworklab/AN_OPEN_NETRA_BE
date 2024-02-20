import subprocess
import json
from django.conf import settings ###Influx
from influxdb_client import InfluxDBClient ###Influx
from influxdb_client.client.write_api import SYNCHRONOUS ###Influx

def check_helm_deployment_exists(deployment_name, namespace):
    try:
        result = subprocess.run(
            ["helm", "list", "--namespace", namespace, "-q"],
            capture_output=True, text=True
        )
        return deployment_name in result.stdout.split()
    except subprocess.CalledProcessError:
        return False

def write_data_to_influx():
    with InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = "mem,host=host1 used_percent=23.43234543"
        write_api.write(bucket=settings.INFLUXDB_BUCKET, org=settings.INFLUXDB_ORG, record=point)

def query_data_from_influx():
    with InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG) as client:
        query = f'from(bucket: "{settings.INFLUXDB_BUCKET}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "mem")'
        query_api = client.query_api()
        result = query_api.query(org=settings.INFLUXDB_ORG, query=query)
        for table in result:
            for record in table.records:
                print(f'Time: {record.get_time()}, Value: {record.get_value()}')
