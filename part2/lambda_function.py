import json
import boto3

file_name = "vehicle.csv"
bucket_name = "emissions-data-dropoff"
region_name = "us-west-2"

iotclient = boto3.client("iot-data", region_name=region_name)
s3client = boto3.client("s3", region_name=region_name)

fileobj = s3client.get_object(Bucket=bucket_name, Key=file_name)
filedata = fileobj["Body"].read()
contents = filedata.decode("utf-8")
a = contents.split()
emissions_max = str(max(float(x.split(",")[2]) for x in a[1:]))

response = iotclient.publish(
    topic="emissions/max",
    qos=0,
    payload=json.dumps({"max_co2_emission": emissions_max}),
)


def lambda_handler(event, context):
    return

